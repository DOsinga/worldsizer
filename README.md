# World Sizer

World Sizer and Gapmover are two views of one cartogram system:

- [World Sizer](https://douwe.com/projects/worldsizer) compares measurements
  such as population, GDP, and carbon emissions.
- [Gapmover](https://douwe.com/projects/gapmover#1800) shows world population
  from 1800 to 2100.

Cartograms are generated offline in Python. The browser loads precomputed
coordinates and uses one small player to draw and animate both pages.

## Repository layout

- `static/geometry.json` — canonical, content-versioned geometry
- `static/cartogram-player.js` — shared browser renderer and player
- `static/population_frames.json` — preserved Gapmover timeline
- `static/measurement_paths.json` — generated World Sizer relaxation paths
- `data/population.json` — legacy population inputs
- `data/measurements.json` — legacy World Sizer measurement inputs
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

## Generate measurement paths

```bash
python generate.py measurements
```

The default produces five relaxation checkpoints for raw and
density-corrected variants of each retained measurement. The resulting bundle
is below the 1 MB compressed size budget.

## Compare with the shipped population frames

```bash
python generate.py compare-population
```

This applies the canonical country-code mappings and initializes each year from
the preceding result, matching the timeline's generation model. It writes
maximum, median, and RMS point displacement to `baseline/comparison/report.json`.
Add `--render` for shipped, generated, and pixel-difference PNGs. The PNGs are
ignored by Git.

Use `--bridges canonical` to test the current bridge constraints instead of the
ones used by the legacy population frames, or `--mode independent` to test each
year from the base map.
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
