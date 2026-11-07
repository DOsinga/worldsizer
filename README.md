# World Sizer

World Sizer and Gapmover are two views of one cartogram system:

- [World Sizer](https://douwe.com/projects/worldsizer) compares measurements
  such as population, GDP, and carbon emissions.
- [Gapmover](https://douwe.com/projects/gapmover#1800) shows world population
  from 1800 to 2100.

Cartograms are generated offline in Python. The browser loads precomputed
coordinates and uses one small player to draw and animate both pages.

## Run locally

```bash
uvx douwe worldsizer
uvx douwe gapmover
```

## Repository layout

- `static/geometry.json` — canonical, content-versioned geometry
- `static/cartogram-player.js` — shared browser renderer and player
- `static/population_frames.json` — generated Gapmover timeline
- `baseline/population_frames.json.gz` — preserved legacy Gapmover timeline
- `static/measurement_paths.json` — generated World Sizer relaxation paths
- `data/population.json` — legacy population inputs
- `data/measurements.json` — assembled World Sizer measurement inputs
- `update_sources.py` — downloads maintained World Bank and EIA source snapshots
- `build_measurements.py` — assembles source snapshots into World Sizer inputs
- `cartogram.py` — Python port of the original force solver
- `generate.py` — frame generation and baseline comparison commands
- `worldparser.py` — canonical geometry generator
- `data/ne_110m_admin_0_countries.*` — Natural Earth source geometry
- `DESIGN.md` — architecture and migration decisions
- `DATA.md` — provenance, known gaps, and legacy data rules

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip sync requirements.txt
```

After changing `requirements.in`, regenerate the resolved dependencies with
`uv pip compile requirements.in -o requirements.txt`.

## Update measurement sources

```bash
python update_sources.py
```

This downloads the latest available values from World Bank Open Data, EIA's
public International bulk dataset, and Medals per Capita. It writes normalized,
country-mapped snapshots to `data/sources/`, including the source, indicator,
unit, observation year, and missing countries for every fact. Use `world-bank`,
`eia`, or `olympics` as the command argument to update only one provider.

Then assemble the player input and generate its paths:

```bash
python build_measurements.py
python generate.py measurements
```

## Generate measurement paths

```bash
python generate.py measurements
```

The default produces five relaxation checkpoints for each retained
measurement. The resulting bundle is below the 1.5 MB compressed size budget.

## Compare with the shipped population frames

```bash
python generate.py compare-population
```

This applies the canonical country-code mappings and initializes each year from
the preceding result, matching the timeline's generation model. It writes
maximum, median, and RMS point displacement to `baseline/comparison/report.json`.
Add `--render` for shipped, generated, and pixel-difference PNGs. The PNGs are
ignored by Git.

## Generate the population timeline

```bash
python generate.py population
```

This generates each 1800–2100 frame independently with the canonical bridges
and layout rules, then projects the shapes back onto their scaled templates to
remove long folded edges. The preserved legacy frames remain the comparison
baseline.

Use `--bridges canonical` to test the current bridge constraints instead of the
ones used by the legacy population frames, or `--mode independent` to test each
year from the base map.
Use `--layout expanded` to include the Indonesia layout rule used by newly
generated measurement paths; the default fixed layout matches the legacy
population solver.
Use `--year 1800` for a quick single-frame check; a single later year also starts
from the base map because its preceding frames were not generated.

## Audit data coverage

```bash
python generate.py audit
```

This records missing and zero values for every retained measurement and every
population frame in `baseline/data_audit.json`.

## Test

```bash
python -m unittest discover -s tests -v
```

The integration test checks the Python port against a reference tick from the
original JavaScript solver to twelve decimal places.
