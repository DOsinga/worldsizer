# Data

## Geometry

`static/geometry.json` is the canonical snapshot generated from Natural Earth
geometry by the original 2020 pipeline. `worldparser.py` reproduces its 175
country records, topology, bridges, and 7,491 shared points in a Mollweide
projection. Current projection libraries differ from the snapshot by at most
2e-15 in normalized coordinates; the tolerance is covered by a test.

The geometry version is derived from a hash of its countries and points. Any
geometry change therefore requires matching frames instead of silently passing
the player's compatibility check.

The earlier numbered geometry files used the same polygons and points. Their
last topology change added solver bridges connecting Senegal to Brazil, Italy
to Spain, and Iran to Qatar. The current solver geometry also anchors Iceland
to Great Britain, ties Lesotho's shared inner ring to South Africa's outer
ring.

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
is missing. They render against the canonical geometry but record
`solverBridges: legacy` because they retain the earlier bridge configuration.

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

`data/data_issues.json` records values corrected or ignored during the legacy
import. The audit also reports every non-numeric value, including values in
fields that are not offered by the site.
