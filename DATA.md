# Data

## Geometry

`static/geometry.json` is `world-006`, generated from Natural Earth geometry by
`worldparser.py`. It contains 175 country records and 7,491 shared points in a
Mollweide projection.

The earlier numbered geometry files used the same polygons and points. The
canonical version adds three solver bridges connecting Senegal to Brazil,
Italy to Spain, and Iran to Qatar.

## Population timeline

`data/population.json` is the historical and projected population input used by
the original Gapmover. Its original source and normalization procedure have not
yet been recovered.

Historical records do not cover every present-day country. The legacy solver
uses the average target multiplier of the country's continent when a value is
missing. This policy is retained only to reproduce the current output. New
population data needs an explicit mapping for historical predecessors before
it replaces the legacy data.

`data/country_mappings.json` resolves five obsolete or project-specific codes
to the canonical geometry. It also records the remaining continent-average
fallback as an explicit legacy policy. `python generate.py audit` writes every
case to `baseline/data_audit.json` so it cannot pass unnoticed.

`static/population_frames.json` contains the shipped 1800–2100 frames. They are
preserved as the visual baseline even though their original generation harness
is missing.

## World Sizer measurements

`data/measurements.json` is the dataset currently served by World Sizer. The
script that produced it is missing. The old CIA Factbook scraper and combination
script did not reproduce its fields or country set and have therefore been
removed.

`data/measurement_manifest.json` lists the fields retained by the new player.
Productive land area is removed because the served dataset has no values for
it. Each remaining field still needs a source and date before the data can be
described as reproducible or updated safely.

The legacy density correction is also preserved: records with zero population
are left uncorrected. The data audit must identify those records before a new
dataset replaces this behavior.

The baseline measurement paths run the ported solver for 299 ticks, matching
the old browser loop's initial history frame plus 299 generated frames. Five
checkpoints per path keep the compressed frame bundle below the 1 MB budget.

`data/data_issues.json` records values corrected during the legacy import.
Currently this contains Somalia's empty-string `Living with Aids` value, which
is treated as missing. Leaving the empty string in place makes JavaScript turn
the normalization sum into string concatenation.
