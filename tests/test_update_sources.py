import unittest

from build_measurements import build_measurements
from update_sources import (
    eia_values,
    historical_olympic_values,
    iso3_to_geometry,
    latest_world_bank_values,
)


class UpdateSourcesTest(unittest.TestCase):
    def test_world_bank_uses_latest_country_value_and_maps_project_codes(self):
        rows = [
            {"country": {"id": "YE"}, "date": "2022", "value": 20},
            {"country": {"id": "YE"}, "date": "2023", "value": 30},
            {"country": {"id": "US"}, "date": "2023", "value": None},
            {"country": {"id": "ZH"}, "date": "2023", "value": 100},
        ]
        values = latest_world_bank_values(
            rows,
            {"ry": "Yemen", "us": "United States"},
            {"ye": "ry"},
        )

        self.assertEqual(values, {
            "ry": {"name": "Yemen", "year": 2023, "value": 30},
        })

    def test_eia_uses_world_bank_iso3_mapping_and_keeps_zero(self):
        countries = [
            {
                "id": "YEM",
                "iso2Code": "YE",
                "region": {"value": "Middle East & North Africa"},
            },
            {
                "id": "WLD",
                "iso2Code": "1W",
                "region": {"value": "Aggregates"},
            },
        ]
        names = {"ry": "Yemen", "tw": "Taiwan"}
        mapping = iso3_to_geometry(countries, names, {"ye": "ry"})
        values = eia_values(
            [
                {
                    "geography": "YEM",
                    "geoset_id": "INTL.57-1-TBPD.A",
                    "data": [["2023", 0], ["2022", 1]],
                },
                {
                    "geography": "TWN",
                    "geoset_id": "INTL.57-1-TBPD.A",
                    "data": [["2023", 0.196]],
                },
            ],
            mapping,
            names,
            2023,
        )

        self.assertEqual(mapping["YEM"], "ry")
        self.assertEqual(mapping["TWN"], "tw")
        self.assertEqual(values["ry"]["value"], 0)
        self.assertEqual(values["ry"]["year"], 2023)
        self.assertEqual(values["tw"]["value"], 0.196)

    def test_olympic_totals_include_summer_and_winter_through_reference_year(self):
        data = [
            [
                "Country", "Code", "2024 Paralympics Gold", "2024 Gold",
                "2022 Gold", "1992W Silver", "2026 Gold",
            ],
            ["", "", "", "", "", "", ""],
            ["United States", "USA", "9", "3", "2", "1", "8"],
        ]

        values = historical_olympic_values(
            data,
            {"USA": "us"},
            {"us": "United States", "gl": "Greenland"},
            2024,
        )

        self.assertEqual(values["us"]["value"], 6)
        self.assertEqual(values["gl"]["value"], 0)

    def test_measurement_build_uses_sources_and_omits_retired_fields(self):
        geometry = {
            "countries": [
                {"cc": "af", "name": "Afghanistan", "weight": 0.4},
                {"cc": "ry", "name": "Yemen", "weight": 0.6},
            ]
        }
        world_bank = {"fields": {
            field: {"values": {}}
            for field in (
                "population", "surface_area", "co2_emissions", "armed_forces",
                "gdp", "people_living_with_hiv", "exports", "labor_force",
                "forest_area", "alcohol_per_capita",
            )
        }}
        world_bank["fields"]["population"]["values"]["af"] = {"value": 10}
        world_bank["fields"]["surface_area"]["values"]["af"] = {"value": 20}
        world_bank["fields"]["forest_area"]["values"]["af"] = {"value": 5}
        world_bank["fields"]["alcohol_per_capita"]["values"]["af"] = {"value": 2}
        eia = {"fields": {"oil_production": {"values": {"af": {"value": 3}}}}}

        olympics = {"fields": {"olympic_medals": {"values": {
            "af": {"value": 2},
            "ry": {"value": 0},
        }}}}
        measurements = build_measurements(
            geometry,
            world_bank,
            eia,
            olympics,
            {"ye": "ry"},
        )

        self.assertEqual(measurements["af"]["Area"], 20)
        self.assertEqual(measurements["af"]["Forest area"], 5)
        self.assertEqual(measurements["af"]["Oil production"], 3)
        self.assertEqual(measurements["af"]["Alcohol consumption"], 20)
        self.assertEqual(measurements["ry"]["Olympic medals"], 0)
        self.assertNotIn("Covid Cases", measurements["af"])


if __name__ == "__main__":
    unittest.main()
