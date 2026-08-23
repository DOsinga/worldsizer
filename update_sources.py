import argparse
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from datetime import date
from pathlib import Path


ROOT = Path(__file__).parent
REFERENCE_YEAR = 2025
LOOKBACK_YEARS = 7
EIA_COUNTRY_OVERRIDES = {
    "ATA": "aq",
    "ESH": "eh",
    "FLK": "fk",
    "TWN": "tw",
    "XKS": "kv",
}

WORLD_BANK_FIELDS = {
    "population": {
        "indicator": "SP.POP.TOTL",
        "label": "Population, total",
        "unit": "people",
    },
    "surface_area": {
        "indicator": "AG.SRF.TOTL.K2",
        "label": "Surface area",
        "unit": "square kilometres",
    },
    "land_area": {
        "indicator": "AG.LND.TOTL.K2",
        "label": "Land area",
        "unit": "square kilometres",
    },
    "co2_emissions": {
        "indicator": "EN.GHG.CO2.MT.CE.AR5",
        "label": "Carbon dioxide emissions excluding land-use change",
        "unit": "million tonnes CO2 equivalent",
    },
    "armed_forces": {
        "indicator": "MS.MIL.TOTL.P1",
        "label": "Armed forces personnel, total",
        "unit": "people",
    },
    "gdp": {
        "indicator": "NY.GDP.MKTP.CD",
        "label": "GDP",
        "unit": "current US dollars",
    },
    "people_living_with_hiv": {
        "indicator": "SH.DYN.AIDS",
        "label": "People living with HIV, total",
        "unit": "people",
    },
    "exports": {
        "indicator": "NE.EXP.GNFS.CD",
        "label": "Exports of goods and services",
        "unit": "current US dollars",
    },
    "alcohol_per_capita": {
        "indicator": "SH.ALC.PCAP.LI",
        "label": "Alcohol consumption per person aged 15 or older",
        "unit": "litres of pure alcohol per year",
    },
    "labor_force": {
        "indicator": "SL.TLF.TOTL.IN",
        "label": "Labor force, total",
        "unit": "people",
    },
    "forest_area": {
        "indicator": "AG.LND.FRST.K2",
        "label": "Forest area",
        "unit": "square kilometres",
    },
}


def read_json(path):
    with open(path) as source:
        return json.load(source)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as destination:
        json.dump(value, destination, indent=2, sort_keys=True)
        destination.write("\n")


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "worldsizer-data/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": "worldsizer-data/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode()


def country_context():
    geometry = read_json(ROOT / "static/geometry.json")
    mappings = read_json(ROOT / "data/country_mappings.json")["sourceToGeometry"]
    names = {country["cc"]: country["name"] for country in geometry["countries"]}
    return names, mappings


def canonical_code(source_code, mappings):
    source_code = source_code.lower()
    return mappings.get(source_code, source_code)


def latest_world_bank_values(rows, country_names, mappings):
    values = {}
    for row in rows:
        if row["value"] is None:
            continue
        country_code = canonical_code(row["country"]["id"], mappings)
        if country_code not in country_names:
            continue
        observation = {
            "name": country_names[country_code],
            "year": int(row["date"]),
            "value": row["value"],
        }
        if country_code not in values or observation["year"] > values[country_code]["year"]:
            values[country_code] = observation
    return values


def world_bank_url(indicator, reference_year, lookback_years):
    start_year = reference_year - lookback_years + 1
    query = urllib.parse.urlencode({
        "format": "json",
        "date": f"{start_year}:{reference_year}",
        "per_page": 20000,
    })
    return f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?{query}"


def fetch_world_bank(reference_year, lookback_years):
    country_names, mappings = country_context()
    fields = {}
    for field, details in WORLD_BANK_FIELDS.items():
        url = world_bank_url(details["indicator"], reference_year, lookback_years)
        payload = fetch_json(url)
        if len(payload) != 2:
            raise ValueError(f"World Bank returned no data for {details['indicator']}")
        values = latest_world_bank_values(payload[1], country_names, mappings)
        fields[field] = {
            **details,
            "sourceUrl": f"https://data.worldbank.org/indicator/{details['indicator']}",
            "values": values,
            "missing": sorted(set(country_names) - set(values)),
        }
    return {
        "source": "World Bank Open Data",
        "license": "CC BY 4.0",
        "retrieved": date.today().isoformat(),
        "referenceYear": reference_year,
        "lookbackYears": lookback_years,
        "fields": fields,
    }


def world_bank_countries():
    payload = fetch_json("https://api.worldbank.org/v2/country?format=json&per_page=400")
    return payload[1]


def iso3_to_geometry(countries, country_names, mappings):
    result = {
        source_code: country_code
        for source_code, country_code in EIA_COUNTRY_OVERRIDES.items()
        if country_code in country_names
    }
    for country in countries:
        if country["region"]["value"] == "Aggregates":
            continue
        country_code = canonical_code(country["iso2Code"], mappings)
        if country_code in country_names:
            result[country["id"]] = country_code
    return result


def eia_values(series, code_mapping, country_names, reference_year):
    values = {}
    for row in series:
        country_code = code_mapping.get(row.get("geography"))
        if country_code is None or row.get("geoset_id") != "INTL.57-1-TBPD.A":
            continue
        observation = next(
            (value for year, value in row["data"] if int(year) == reference_year),
            None,
        )
        if observation is None:
            continue
        values[country_code] = {
            "name": country_names[country_code],
            "year": reference_year,
            "value": observation,
        }
    return values


def fetch_eia(reference_year):
    country_names, mappings = country_context()
    code_mapping = iso3_to_geometry(world_bank_countries(), country_names, mappings)
    source_url = "https://www.eia.gov/opendata/bulk/INTL.zip"
    request = urllib.request.Request(source_url, headers={"User-Agent": "worldsizer-data/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        archive_data = response.read()
    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        with archive.open("INTL.txt") as source:
            series = (json.loads(line) for line in source)
            values = eia_values(series, code_mapping, country_names, reference_year)
    return {
        "source": "U.S. Energy Information Administration",
        "sourceUrl": "https://www.eia.gov/international/data/world/petroleum-and-other-liquids/annual-petroleum-and-other-liquids-production",
        "downloadUrl": source_url,
        "dataset": "International Energy Data bulk download",
        "retrieved": date.today().isoformat(),
        "referenceYear": reference_year,
        "fields": {
            "oil_production": {
                "label": "Crude oil production including lease condensate",
                "unit": "thousand barrels per day",
                "activityId": "1",
                "productId": "57",
                "values": values,
                "missing": sorted(set(country_names) - set(values)),
            }
        },
    }


def historical_olympic_values(data, code_mapping, country_names, reference_year):
    header = data[0]
    medal_columns = [
        index
        for index, label in enumerate(header)
        if (
            (match := re.fullmatch(r"(\d{4})(?:W)? (?:Gold|Silver|Bronze)", label))
            and int(match.group(1)) <= reference_year
        )
    ]
    values = {
        country_code: {
            "name": name,
            "year": reference_year,
            "value": 0,
        }
        for country_code, name in country_names.items()
    }
    for row in data[2:]:
        if len(row) < 2:
            continue
        country_code = code_mapping.get(row[1])
        if country_code is None:
            continue
        values[country_code]["value"] = sum(
            int(float(row[index])) for index in medal_columns if row[index]
        )
    return values


def fetch_olympics(reference_year):
    country_names, mappings = country_context()
    code_mapping = iso3_to_geometry(world_bank_countries(), country_names, mappings)
    source_url = "https://historical.medalspercapita.com/data.js"
    source = fetch_text(source_url)
    data = json.loads(source.partition("=")[2].strip().removesuffix(";"))
    data_year = max(
        int(match.group(1))
        for label in data[0]
        if (match := re.fullmatch(r"(\d{4})(?:W)? (?:Gold|Silver|Bronze)", label))
        and int(match.group(1)) <= reference_year
    )
    values = historical_olympic_values(
        data,
        code_mapping,
        country_names,
        data_year,
    )
    return {
        "source": "Craig Nevill-Manning's Medals per Capita",
        "sourceUrl": "https://historical.medalspercapita.com/",
        "downloadUrl": source_url,
        "retrieved": date.today().isoformat(),
        "referenceYear": data_year,
        "fields": {
            "olympic_medals": {
                "label": "Olympic medals won across all Summer and Winter Games",
                "unit": "medals",
                "values": values,
                "missing": [],
            }
        },
    }


def parser():
    result = argparse.ArgumentParser(description="Fetch maintained World Sizer data sources")
    result.add_argument(
        "source",
        choices=("world-bank", "eia", "olympics", "all"),
        nargs="?",
        default="all",
    )
    result.add_argument("--reference-year", type=int, default=REFERENCE_YEAR)
    result.add_argument("--lookback-years", type=int, default=LOOKBACK_YEARS)
    return result


def main():
    args = parser().parse_args()
    if args.source in {"world-bank", "all"}:
        snapshot = fetch_world_bank(args.reference_year, args.lookback_years)
        write_json(ROOT / "data/sources/world_bank.json", snapshot)
    if args.source in {"eia", "all"}:
        snapshot = fetch_eia(args.reference_year)
        write_json(ROOT / "data/sources/eia.json", snapshot)
    if args.source in {"olympics", "all"}:
        snapshot = fetch_olympics(args.reference_year)
        write_json(ROOT / "data/sources/olympic_medals.json", snapshot)


if __name__ == "__main__":
    main()
