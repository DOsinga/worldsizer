import hashlib
import json
import math
from statistics import median


COLORS = {
    "Africa": "#D03030",
    "Europe": "#7E5E58",
    "Americas": "#00CC00",
    "Asia": "#3030DC",
    "Antarctica": "#AF00AF",
    "Oceania": "#00AFAF",
    "Seven seas (open ocean)": "#AFAF00",
}

EXPANDED_COUNTRY_LAYOUTS = {"id"}


def geometry_version(geometry):
    content = json.dumps(
        {"countries": geometry["countries"], "points": geometry["points"]},
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return f"world-{hashlib.sha256(content).hexdigest()[:12]}"


def normalized_weights(data, field):
    weights = {}
    for country_code, values in data.items():
        if field not in values:
            continue
        value = values[field]
        weights[country_code] = value
    total = sum(weights.values())
    if not math.isfinite(total) or total <= 0:
        raise ValueError(f"{field} has no positive finite total")
    return {country_code: value / total for country_code, value in weights.items()}


def population_backfilled_weights(data, countries, field):
    continent_values = {}
    continent_populations = {}
    for country in countries:
        values = data[country["cc"]]
        value = values.get(field)
        population = values.get("Population")
        if not isinstance(value, (int, float)) or not population:
            continue
        continent = country["continent"]
        continent_values[continent] = continent_values.get(continent, 0) + value
        continent_populations[continent] = continent_populations.get(continent, 0) + population

    filled = {}
    for country in countries:
        country_code = country["cc"]
        values = data[country_code]
        if field in values or not values.get("Population"):
            filled[country_code] = values
            continue
        continent = country["continent"]
        if not continent_populations.get(continent):
            filled[country_code] = values
            continue
        filled[country_code] = {
            **values,
            field: (
                values["Population"]
                * continent_values[continent]
                / continent_populations[continent]
            ),
        }
    return normalized_weights(filled, field)


def population_weights(data, year):
    index = year - 1800
    if not 0 <= index <= 300:
        raise ValueError(f"population year is outside 1800-2100: {year}")
    weights = {
        country_code: values[index]
        for country_code, values in data.items()
        if index < len(values) and values[index] > 0
    }
    total = sum(weights.values())
    if total <= 0:
        raise ValueError(f"population data is empty for {year}")
    return {country_code: value / total for country_code, value in weights.items()}


def polygon_area(point_indices, points):
    area = 0.0
    for index, point_index in enumerate(point_indices):
        next_index = point_indices[(index + 1) % len(point_indices)]
        point = points[point_index]
        next_point = points[next_index]
        area += point[0] * next_point[1] - next_point[0] * point[1]
    return abs(area) / 2


class Cartogram:
    def __init__(
        self,
        geometry,
        *,
        initial=None,
        max_speed=0.002,
        legacy_zero_missing=False,
        expand_country_layout=True,
    ):
        self.base = geometry["points"]
        self.points = [list(point) for point in initial or self.base]
        self.countries = geometry["countries"]
        self.country_codes = {country["cc"] for country in self.countries}
        self.max_speed = max_speed
        self.legacy_zero_missing = legacy_zero_missing
        self.expand_country_layout = expand_country_layout
        self.country_centers = []
        for country in self.countries:
            area = sum(shape["area"] for shape in country["shapes"])
            self.country_centers.append((
                sum(shape["x"] * shape["area"] for shape in country["shapes"]) / area,
                sum(shape["y"] * shape["area"] for shape in country["shapes"]) / area,
            ))
        self.multipliers = []
        self.loss = 0.0

    def set_target_weights(self, target_weights):
        continent_weights = {}
        continent_targets = {}
        for country in self.countries:
            target = target_weights.get(country["cc"])
            present = bool(target) if self.legacy_zero_missing else country["cc"] in target_weights
            if present:
                continent = country["continent"]
                continent_weights.setdefault(continent, []).append(country["weight"])
                continent_targets.setdefault(continent, []).append(target)

        continent_multipliers = {
            continent: sum(continent_targets[continent]) / sum(weights)
            for continent, weights in continent_weights.items()
        }

        self.multipliers = []
        for country in self.countries:
            country_code = country["cc"]
            target = target_weights.get(country_code)
            present = bool(target) if self.legacy_zero_missing else country_code in target_weights
            if present:
                multiplier = target / country["weight"]
            else:
                multiplier = continent_multipliers.get(country["continent"])
                if not multiplier and country["continent"] == "Antarctica":
                    multiplier = 0.0
                elif not multiplier and country["continent"] == "Seven seas (open ocean)":
                    multiplier = continent_multipliers.get("Oceania")
            if multiplier is None:
                raise ValueError(f"no target or fallback for {country_code}")
            self.multipliers.append(multiplier)

    def tick(self):
        deltas = [None] * len(self.points)
        self.loss = 0.0

        for country_index, country in enumerate(self.countries):
            multiplier = self.multipliers[country_index]
            target_sqrt = math.sqrt(multiplier)
            country_x, country_y = self.country_centers[country_index]
            for shape in country["shapes"]:
                shape_points = shape["pts"]
                center_x = sum(self.points[index][0] for index in shape_points) / len(shape_points)
                center_y = sum(self.points[index][1] for index in shape_points) / len(shape_points)
                if self.expand_country_layout and country["cc"] in EXPANDED_COUNTRY_LAYOUTS:
                    target_x = country_x + (shape["x"] - country_x) * target_sqrt
                    target_y = country_y + (shape["y"] - country_y) * target_sqrt
                else:
                    target_x = shape["x"]
                    target_y = shape["y"]
                home_x = target_x - center_x
                home_y = target_y - center_y
                bridge_sum_x = 0.0
                bridge_sum_y = 0.0

                for anchor_index, offset_x, offset_y, country_code in shape["bridges"]:
                    if country_code not in self.country_codes:
                        continue
                    anchor_x, anchor_y = self.points[anchor_index]
                    bridge_sum_x -= offset_x * target_sqrt - (anchor_x - center_x)
                    bridge_sum_y -= offset_y * target_sqrt - (anchor_y - center_y)

                current_area = polygon_area(shape_points, self.points)
                if current_area == 0 and multiplier == 0:
                    continue
                ratio = current_area / shape["area"]
                grow_sqrt = math.sqrt(multiplier / ratio) - 1
                self.loss += abs(grow_sqrt) * shape["area"] * multiplier

                for point_index in shape_points:
                    base_x, base_y = self.base[point_index]
                    point_x, point_y = self.points[point_index]
                    relative_x = point_x - center_x
                    relative_y = point_y - center_y
                    shape_pull_x = (base_x - shape["x"]) * target_sqrt - relative_x
                    shape_pull_y = (base_y - shape["y"]) * target_sqrt - relative_y
                    delta_x = (
                        relative_x * grow_sqrt * 0.20
                        + shape_pull_x
                        + bridge_sum_x * 20
                        + home_x * 0.03
                    )
                    delta_y = (
                        relative_y * grow_sqrt * 0.20
                        + shape_pull_y
                        + bridge_sum_y * 20
                        + home_y * 0.03
                    )
                    point_delta = deltas[point_index]
                    if point_delta is None:
                        deltas[point_index] = [delta_x, delta_y]
                    else:
                        point_delta[0] += delta_x
                        point_delta[1] += delta_y

        next_points = []
        for point, delta in zip(self.points, deltas):
            if delta is None:
                next_points.append(point)
                continue
            dx, dy = delta
            distance = math.hypot(dx, dy)
            if distance > self.max_speed:
                dx *= self.max_speed / distance
                dy *= self.max_speed / distance
            next_points.append([point[0] + dx, point[1] + dy])
        self.points = next_points
        return self.loss

    def project_shapes(self, iterations):
        for _ in range(iterations):
            projected = [[0.0, 0.0, 0] for _ in self.points]
            for country_index, country in enumerate(self.countries):
                scale = math.sqrt(self.multipliers[country_index])
                for shape in country["shapes"]:
                    shape_points = shape["pts"]
                    center_x = sum(self.points[index][0] for index in shape_points) / len(shape_points)
                    center_y = sum(self.points[index][1] for index in shape_points) / len(shape_points)
                    for point_index in shape_points:
                        point = projected[point_index]
                        point[0] += center_x + (self.base[point_index][0] - shape["x"]) * scale
                        point[1] += center_y + (self.base[point_index][1] - shape["y"]) * scale
                        point[2] += 1
            self.points = [
                [x / count, y / count] if count else point
                for point, (x, y, count) in zip(self.points, projected)
            ]
        return self.points

    def run(self, ticks, capture_every=None):
        frames = []
        for tick in range(1, ticks + 1):
            self.tick()
            if capture_every and (tick % capture_every == 0 or tick == ticks):
                frames.append([point[:] for point in self.points])
        return frames


def displacement(generated, expected, scale=10000):
    distances = [
        math.hypot(
            generated[index][0] * scale - expected[index][0],
            generated[index][1] * scale - expected[index][1],
        )
        for index in range(len(generated))
    ]
    return {
        "maximum": max(distances),
        "median": median(distances),
        "rms": math.sqrt(sum(distance * distance for distance in distances) / len(distances)),
    }


def quantize(points, scale=10000):
    return [[round(point[0] * scale), round(point[1] * scale)] for point in points]


def flatten(points):
    return [coordinate for point in points for coordinate in point]


def delta_frames(base, frames, scale=10000):
    previous = quantize(base, scale)
    encoded = []
    for frame in frames:
        current = quantize(frame, scale)
        encoded.append(
            flatten(
                [
                    [point[0] - old[0], point[1] - old[1]]
                    for point, old in zip(current, previous)
                ]
            )
        )
        previous = current
    return encoded
