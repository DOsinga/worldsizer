import json
from pathlib import Path


ROOT = Path(__file__).parent
EARTH_LAND_AREA = 149_000_000

WORLD_BANK_FIELDS = {
    "Population": "population",
    "CO2 emissions": "co2_emissions",
    "Armed forces": "armed_forces",
    "GDP": "gdp",
    "People living with HIV": "people_living_with_hiv",
    "Exports": "exports",
    "Labor force": "labor_force",
    "Forest area": "forest_area",
}


def read_json(path):
    with open(path) as source:
        return json.load(source)


def write_json(path, value):
    with open(path, "w") as destination:
        json.dump(value, destination, indent=2, sort_keys=True)
        destination.write("\n")


def source_values(snapshot, field):
    return snapshot["fields"][field]["values"]


def canonical_values(values, mappings):
    return {
        mappings.get(country_code, country_code): value
        for country_code, value in values.items()
    }


def build_measurements(geometry, world_bank, eia, olympics, mappings):
    country_names = {country["cc"]: country["name"] for country in geometry["countries"]}
    geometry_area = {
        country["cc"]: country["weight"] * EARTH_LAND_AREA
        for country in geometry["countries"]
    }
    fields = {
        output_field: source_values(world_bank, source_field)
        for output_field, source_field in WORLD_BANK_FIELDS.items()
    }
    areas = source_values(world_bank, "surface_area")
    alcohol = source_values(world_bank, "alcohol_per_capita")
    oil = source_values(eia, "oil_production")
    olympic_medals = source_values(olympics, "olympic_medals")
    measurements = {}

    for country_code, name in country_names.items():
        values = {
            "Iso2": country_code.upper(),
            "wiki_id": name,
            "Area": areas.get(country_code, {"value": geometry_area[country_code]})["value"],
        }
        for output_field, source in fields.items():
            if country_code in source:
                values[output_field] = source[country_code]["value"]
        if country_code in alcohol and "Population" in values:
            values["Alcohol consumption"] = alcohol[country_code]["value"] * values["Population"]
        if country_code in oil:
            values["Oil production"] = oil[country_code]["value"]
        if country_code in olympic_medals:
            values["Olympic medals"] = olympic_medals[country_code]["value"]
        measurements[country_code] = values
    return measurements


def main():
    mappings = read_json(ROOT / "data/country_mappings.json")["sourceToGeometry"]
    measurements = build_measurements(
        read_json(ROOT / "static/geometry.json"),
        read_json(ROOT / "data/sources/world_bank.json"),
        read_json(ROOT / "data/sources/eia.json"),
        read_json(ROOT / "data/sources/olympic_medals.json"),
        mappings,
    )
    write_json(ROOT / "data/measurements.json", measurements)


if __name__ == "__main__":
    main()
