import argparse
import copy
import json
from pathlib import Path

from cartogram import (
    COLORS,
    Cartogram,
    delta_frames,
    displacement,
    normalized_weights,
    population_weights,
)


ROOT = Path(__file__).parent


def load_json(path):
    with open(path) as source:
        return json.load(source)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as destination:
        json.dump(value, destination, separators=(",", ":"))


def canonical_codes(data, mappings):
    source_to_geometry = mappings["sourceToGeometry"]
    return {
        source_to_geometry.get(country_code, country_code): values
        for country_code, values in data.items()
    }


def legacy_geometry(geometry):
    geometry = copy.deepcopy(geometry)
    for country in geometry["countries"]:
        if country["cc"] in {"br", "es", "ir"}:
            country["shapes"][0]["bridges"] = []
    return geometry


def generate_measurements(args):
    geometry = load_json(ROOT / "static/geometry.json")
    mappings = load_json(ROOT / "data/country_mappings.json")
    measurements = canonical_codes(load_json(ROOT / "data/measurements.json"), mappings)
    manifest = load_json(ROOT / "data/measurement_manifest.json")
    paths = {}

    for measurement in manifest["measurements"]:
        field = measurement["id"]
        if field == "Area":
            continue
        for density in (False, True):
            key = f"{field}:density" if density else field
            solver = Cartogram(geometry, max_speed=args.max_speed)
            solver.set_target_weights(normalized_weights(measurements, field, density))
            frames = solver.run(args.ticks, args.capture_every)
            paths[key] = delta_frames(geometry["points"], frames, args.scale)

    output = {
        "geometry": geometry["version"],
        "scale": args.scale,
        "ticks": args.ticks,
        "captureEvery": args.capture_every,
        "missingData": "continent-average",
        "paths": paths,
    }
    write_json(ROOT / args.output, output)
    write_json(ROOT / "static/measurements.json", measurements)


def audit_data(args):
    geometry = load_json(ROOT / "static/geometry.json")
    mappings = load_json(ROOT / "data/country_mappings.json")
    measurements = canonical_codes(load_json(ROOT / "data/measurements.json"), mappings)
    manifest = load_json(ROOT / "data/measurement_manifest.json")
    population = canonical_codes(load_json(ROOT / "data/population.json"), mappings)
    country_codes = {country["cc"] for country in geometry["countries"]}

    measurement_report = {}
    for measurement in manifest["measurements"]:
        field = measurement["id"]
        present = {
            code for code, values in measurements.items()
            if isinstance(values.get(field), (int, float))
        }
        measurement_report[field] = {
            "present": len(present & country_codes),
            "missing": sorted(country_codes - present),
            "zero": sorted(
                code for code in present & country_codes
                if measurements[code][field] == 0
            ),
        }

    years = range(1800, 2101, 20)
    population_report = {}
    for year in years:
        index = year - 1800
        present = {
            code for code, values in population.items()
            if index < len(values) and values[index] > 0
        }
        population_report[str(year)] = {
            "present": len(present & country_codes),
            "missing": sorted(country_codes - present),
        }

    write_json(ROOT / args.output, {
        "geometry": geometry["version"],
        "geometryCountries": len(country_codes),
        "countryMappings": mappings["sourceToGeometry"],
        "unknownMeasurementCountries": sorted(set(measurements) - country_codes),
        "unknownPopulationCountries": sorted(set(population) - country_codes),
        "measurements": measurement_report,
        "population": population_report,
    })


def render(geometry, points, path, *, scale=None):
    from PIL import Image, ImageDraw

    if scale:
        points = [[point[0] / scale, point[1] / scale] for point in points]
    image = Image.new("RGB", (720, 540), "#7785C0")
    draw = ImageDraw.Draw(image)
    for country in geometry["countries"]:
        if country["cc"] == "gl":
            continue
        for shape in country["shapes"]:
            polygon = [
                (
                    1.2 * points[index][0] * 720 - 140,
                    1.2 * points[index][1] * (540 - 70) + 35,
                )
                for index in shape["pts"]
            ]
            draw.polygon(polygon, fill=COLORS[country["continent"]], outline="#303030")
    image.save(path)
    return image


def compare_population(args):
    from PIL import ImageChops

    geometry = load_json(ROOT / "static/geometry.json")
    if args.bridges == "legacy":
        geometry = legacy_geometry(geometry)
    population = load_json(ROOT / "data/population.json")
    shipped = load_json(ROOT / "static/population_frames.json")
    years = [str(args.year)] if args.year else list(shipped["frames"])
    report = {
        "geometry": geometry["version"],
        "bridges": args.bridges,
        "ticks": args.ticks,
        "mode": args.mode,
        "frames": {},
    }
    initial = None
    output_directory = ROOT / args.output
    output_directory.mkdir(parents=True, exist_ok=True)

    for year_text in years:
        year = int(year_text)
        solver = Cartogram(
            geometry,
            initial=initial,
            max_speed=args.max_speed,
            legacy_zero_missing=True,
        )
        solver.set_target_weights(population_weights(population, year))
        solver.run(args.ticks)
        expected = shipped["frames"][year_text]
        metrics = displacement(solver.points, expected, shipped["scale"])
        report["frames"][year_text] = metrics

        generated_image = render(geometry, solver.points, output_directory / f"{year}-generated.png")
        shipped_image = render(
            geometry,
            expected,
            output_directory / f"{year}-shipped.png",
            scale=shipped["scale"],
        )
        ImageChops.difference(generated_image, shipped_image).save(
            output_directory / f"{year}-diff.png"
        )
        if args.mode == "continuation":
            initial = solver.points

    write_json(output_directory / "report.json", report)


def parser():
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(required=True)

    measurements = commands.add_parser("measurements")
    measurements.add_argument("--ticks", type=int, default=299)
    measurements.add_argument("--capture-every", type=int, default=60)
    measurements.add_argument("--max-speed", type=float, default=0.002)
    measurements.add_argument("--scale", type=int, default=10000)
    measurements.add_argument("--output", type=Path, default=Path("static/measurement_paths.json"))
    measurements.set_defaults(run=generate_measurements)

    audit = commands.add_parser("audit")
    audit.add_argument("--output", type=Path, default=Path("baseline/data_audit.json"))
    audit.set_defaults(run=audit_data)

    comparison = commands.add_parser("compare-population")
    comparison.add_argument("--year", type=int)
    comparison.add_argument("--ticks", type=int, default=1001)
    comparison.add_argument("--max-speed", type=float, default=0.0005)
    comparison.add_argument("--bridges", choices=("legacy", "canonical"), default="legacy")
    comparison.add_argument("--mode", choices=("independent", "continuation"), default="independent")
    comparison.add_argument("--output", type=Path, default=Path("baseline/comparison"))
    comparison.set_defaults(run=compare_population)
    return root


if __name__ == "__main__":
    arguments = parser().parse_args()
    arguments.run(arguments)
