import gzip
import json
import math
import unittest
from pathlib import Path

from cartogram import (
    Cartogram,
    geometry_version,
    normalized_weights,
    population_backfilled_weights,
    population_weights,
)
from generate import parser
from worldparser import build_geometry


ROOT = Path(__file__).parent.parent


def load(path):
    with open(ROOT / path) as source:
        return json.load(source)


class CartogramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry = load("static/geometry.json")
        cls.measurements = load("data/measurements.json")

    def test_python_tick_matches_browser_solver(self):
        reference = load("tests/reference_tick.json")
        solver = Cartogram(self.geometry, expand_country_layout=False)
        solver.set_target_weights(reference["weights"])
        solver.tick()

        self.assertAlmostEqual(solver.loss, reference["loss"], places=12)
        for index, expected in zip(reference["indices"], reference["points"]):
            self.assertAlmostEqual(solver.points[index][0], expected[0], places=12)
            self.assertAlmostEqual(solver.points[index][1], expected[1], places=12)

    def test_zero_is_a_real_target(self):
        weights = normalized_weights(self.measurements, "Olympic medals")
        self.assertIn("gl", weights)
        self.assertEqual(weights["gl"], 0)

        solver = Cartogram(self.geometry)
        solver.set_target_weights(weights)
        greenland = next(
            index for index, country in enumerate(self.geometry["countries"])
            if country["cc"] == "gl"
        )
        self.assertEqual(solver.multipliers[greenland], 0)

    def test_missing_measurement_uses_continent_value_per_person(self):
        countries = [
            {"cc": "aa", "continent": "Test"},
            {"cc": "bb", "continent": "Test"},
        ]
        data = {
            "aa": {"Area": 10, "Population": 10, "Fact": 100},
            "bb": {"Area": 10, "Population": 20},
        }

        raw = population_backfilled_weights(data, countries, "Fact")
        self.assertAlmostEqual(raw["aa"], 1 / 3)
        self.assertAlmostEqual(raw["bb"], 2 / 3)

    def test_generated_assets_match_geometry(self):
        population = load("static/population_frames.json")
        paths = load("static/measurement_paths.json")
        manifest = load("data/measurement_manifest.json")
        point_count = len(self.geometry["points"])

        self.assertEqual(self.geometry["version"], geometry_version(self.geometry))
        self.assertEqual(len(self.geometry["countries"]), 175)
        self.assertEqual(point_count, 7491)
        self.assertEqual(population["geometry"], self.geometry["version"])
        self.assertEqual(paths["geometry"], self.geometry["version"])
        self.assertEqual(population["solverBridges"], "canonical")
        self.assertEqual(population["mode"], "independent")
        self.assertEqual(population["ticksPerFrame"], 1001)
        self.assertEqual(population["projectionPasses"], 5)
        self.assertEqual(population["expandedCountryLayouts"], ["id"])
        self.assertEqual(paths["solverBridges"], "canonical")
        self.assertEqual(paths["expandedCountryLayouts"], ["id"])
        self.assertEqual(paths["measurements"], manifest["measurements"])
        self.assertEqual(
            set(paths["paths"]),
            {item["id"] for item in manifest["measurements"] if item["id"] != "Area"},
        )
        self.assertTrue(all(
            measurement.get("source") and measurement.get("year")
            for measurement in paths["measurements"]
        ))
        self.assertTrue(all(len(frame) == point_count for frame in population["frames"].values()))
        self.assertTrue(
            all(
                len(frame) == point_count * 2
                for path in paths["paths"].values()
                for frame in path
            )
        )

        points_2080 = [
            [x / population["scale"], y / population["scale"]]
            for x, y in population["frames"]["2080"]
        ]
        for country_code in ("id", "mm", "my", "ry", "so"):
            country = next(country for country in self.geometry["countries"] if country["cc"] == country_code)
            longest_edge = max(
                math.dist(
                    points_2080[point_index],
                    points_2080[shape["pts"][(index + 1) % len(shape["pts"])]]
                )
                for shape in country["shapes"]
                for index, point_index in enumerate(shape["pts"])
            )
            self.assertLess(longest_edge, 0.05, country_code)
        self.assertTrue(
            all(
                math.isfinite(value)
                for path in paths["paths"].values()
                for frame in path
                for value in frame
            )
        )

        countries = {country["cc"]: country for country in self.geometry["countries"]}
        iceland_bridges = countries["is"]["shapes"][0]["bridges"]
        self.assertEqual({bridge[3] for bridge in iceland_bridges}, {"gb"})
        sumatra = max(
            (shape for shape in countries["id"]["shapes"] if shape["island"]),
            key=lambda shape: shape["area"],
        )
        self.assertEqual({bridge[3] for bridge in sumatra["bridges"]}, {"my"})
        philippines = countries["ph"]["shapes"]
        self.assertTrue(all(
            bridge[3] == "ph"
            for shape in philippines
            for bridge in shape["bridges"]
        ))
        china = max(countries["cn"]["shapes"], key=lambda shape: shape["area"])
        self.assertIn("ph", {bridge[3] for bridge in china["bridges"]})
        lesotho_points = set(countries["ls"]["shapes"][0]["pts"])
        south_africa_inner = next(
            shape for shape in countries["za"]["shapes"]
            if set(shape["pts"]) == lesotho_points
        )
        self.assertEqual({bridge[3] for bridge in south_africa_inner["bridges"]}, {"za"})

    def test_measurement_paths_fit_download_budget(self):
        raw = (ROOT / "static" / "measurement_paths.json").read_bytes()
        self.assertLessEqual(len(gzip.compress(raw)), 1_500_000)

    def test_population_year_must_be_in_range(self):
        population = load("data/population.json")
        with self.assertRaises(ValueError):
            population_weights(population, 1700)
        with self.assertRaises(ValueError):
            population_weights(population, 2101)

    def test_population_comparison_uses_baseline_configuration(self):
        arguments = parser().parse_args(["compare-population"])
        self.assertEqual(arguments.mode, "continuation")
        self.assertEqual(arguments.bridges, "legacy")
        self.assertEqual(arguments.layout, "fixed")

    def test_geometry_source_reproduces_canonical_map(self):
        generated = build_geometry(ROOT / "data" / "ne_110m_admin_0_countries")
        self.assertEqual(
            [country["cc"] for country in generated["countries"]],
            [country["cc"] for country in self.geometry["countries"]],
        )
        self.assertLess(
            max(math.dist(left, right) for left, right in zip(generated["points"], self.geometry["points"])),
            1e-12,
        )
        for generated_country, canonical_country in zip(generated["countries"], self.geometry["countries"]):
            self.assertAlmostEqual(generated_country["weight"], canonical_country["weight"], places=12)
            for generated_shape, canonical_shape in zip(generated_country["shapes"], canonical_country["shapes"]):
                self.assertEqual(generated_shape["pts"], canonical_shape["pts"])
                self.assertEqual(
                    [bridge[0] for bridge in generated_shape["bridges"]],
                    [bridge[0] for bridge in canonical_shape["bridges"]],
                )


if __name__ == "__main__":
    unittest.main()
