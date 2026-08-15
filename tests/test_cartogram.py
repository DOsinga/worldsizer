import gzip
import json
import math
import unittest
from pathlib import Path

from cartogram import Cartogram, normalized_weights


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
        solver = Cartogram(self.geometry)
        solver.set_target_weights(normalized_weights(self.measurements, "Population"))
        solver.tick()

        self.assertAlmostEqual(solver.loss, reference["loss"], places=12)
        for index, expected in zip(reference["indices"], reference["points"]):
            self.assertAlmostEqual(solver.points[index][0], expected[0], places=12)
            self.assertAlmostEqual(solver.points[index][1], expected[1], places=12)

    def test_zero_is_a_real_target(self):
        weights = normalized_weights(self.measurements, "Olympic Medals")
        self.assertIn("al", weights)
        self.assertEqual(weights["al"], 0)

        solver = Cartogram(self.geometry)
        solver.set_target_weights(weights)
        albania = next(
            index for index, country in enumerate(self.geometry["countries"])
            if country["cc"] == "al"
        )
        self.assertEqual(solver.multipliers[albania], 0)

    def test_generated_assets_match_geometry(self):
        population = load("static/population_frames.json")
        paths = load("static/measurement_paths.json")
        point_count = len(self.geometry["points"])

        self.assertEqual(self.geometry["version"], "world-006")
        self.assertEqual(len(self.geometry["countries"]), 175)
        self.assertEqual(point_count, 7491)
        self.assertEqual(population["geometry"], self.geometry["version"])
        self.assertEqual(paths["geometry"], self.geometry["version"])
        self.assertTrue(all(len(frame) == point_count for frame in population["frames"].values()))
        self.assertTrue(
            all(
                len(frame) == point_count * 2
                for path in paths["paths"].values()
                for frame in path
            )
        )
        self.assertTrue(
            all(
                math.isfinite(value)
                for path in paths["paths"].values()
                for frame in path
                for value in frame
            )
        )

    def test_measurement_paths_fit_download_budget(self):
        raw = (ROOT / "static" / "measurement_paths.json").read_bytes()
        self.assertLessEqual(len(gzip.compress(raw)), 1_000_000)


if __name__ == "__main__":
    unittest.main()
