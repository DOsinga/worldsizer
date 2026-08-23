# World Sizer design

World Sizer and Gapmover are two views of the same cartogram system. World
Sizer compares different measurements, while Gapmover shows population over
time. They should share one map, one offline generator, and one browser player.

## Goals

- Preserve the legacy output as a comparison baseline.
- Make cartogram generation offline and reproducible.
- Keep the browser code limited to loading, drawing, and interpolating frames.
- Make every generated frame reproducible from committed source data.
- Preserve country shapes, shared borders, and recognisable geography.
- Keep population changes visually continuous without allowing distortion to
  accumulate over time.

The existing force model and legacy frames provide the baseline. Generator
changes must be measured against them rather than assumed to be better.

## Canonical geometry

There is one canonical world map. It defines:

- countries and their country codes;
- polygon membership;
- shared point indices;
- bridges between land masses; and
- the original projected coordinates.

Every generated cartogram must use the same topology and point ordering. A
frame is therefore only an array of coordinates, with each coordinate referring
to the corresponding point in the canonical map.

The geometry must have a version identifier. Generated datasets record that
identifier so the player cannot combine frames with incompatible geometry.

`static/geometry.json` is the canonical geometry. Its version is a content hash,
so frames cannot claim compatibility after the map changes. Compared with the
old `_001` geometry used by Gapmover, it has the same 175 countries, polygons,
and 7,491 point coordinates in the same order. Bridges are not used when
drawing, so the preserved Gapmover frames render identically against it. The
current solver bridges add explicit constraints for Iceland and Lesotho
alongside the earlier cross-water bridges. The comparison command can restore
the legacy bridge configuration when investigating a difference.

## Baseline generator

The first generator ports the current JavaScript force model to Python without
redesigning it. Its constants and behaviour are part of the baseline.

The original frame-generation harness is missing. A deterministic port alone
does not guarantee the preserved population frames can be reproduced: initialization,
target stepping, tick count, rounding, and possibly an older engine version
also affect the result. Reproducing the current frames is therefore an
acceptance test, not an assumption.

For every frame, the baseline comparison records:

- maximum and median per-point displacement from the shipped coordinates, in
  scaled-integer units.

An optional render pass writes PNGs at 720 x 540 plus pixel-difference images
against the shipped frames.

The coordinate measurements distinguish rounding noise from a different
equilibrium. The render comparison shows whether a numerical difference is
visually important. This gives later generator work a concrete result to beat.

The baseline preserves the current solver design, not necessarily every legacy
pixel forever. If a faithful port cannot reproduce the opaque shipped frames,
its regenerated frames may replace them after reviewing the measurements and
side-by-side renders. The review and decision are recorded with the generated
dataset. Keeping the old frames remains an option if the difference is visibly
worse or cannot be explained.

## Improved generator

Once the baseline is reproducible, we may improve it if specific visual
problems justify doing so. An improved Python generator takes the canonical
geometry and a map of country code to value. Its objective may include:

- error between each country's target and rendered area;
- distortion from the country's canonical shape;
- displacement from its canonical geographic position;
- preservation of shared borders and bridges.

Folds, invalid polygons, and overlaps are validation checks initially. Polygon
intersection checks are expensive and should become an optimization penalty
only if invalid frames are a real problem.

All shape and position penalties are measured against the canonical map, not
against a previously generated frame. This absolute reference prevents drift.

The output for a measurement is a coordinate array plus generation metadata,
including the geometry version, source-data version, objective score, and
generator settings.

## Population timeline

Nearby years can have more than one valid equilibrium. Continuation initially
seemed useful for visual stability, but it accumulated severe folds by the end
of the timeline. Population frames therefore start independently from the
canonical map. Five shape-projection passes then restore local templates and
average shared border points before the frame is saved.

### Detecting drift and unstable equilibria

Independent frames avoid drift but can still settle into different equilibria.
The generator should report objective scores, overlap, invalid shapes, and
movement between neighbouring years. If visual continuity becomes a problem,
the next step is a joint optimization of all years:

```text
sum(cartogram quality for each year)
+ temporal smoothness between neighbouring years
```

Every frame remains anchored to the canonical map while the temporal term
discourages unnecessary movement between adjacent years.

## Independent measurements

World Sizer measurements such as population, GDP, emissions, and army size do
not have a meaningful sequence. Each is generated independently from the
canonical map.

Transitions between measurements pass through the geographic map:

```text
population -> geographic area -> GDP
```

This avoids interpolating directly between unrelated equilibria, where
countries could cross, fold, or move in confusing ways.

The generator can retain every Nth relaxation step between the geographic map
and a measurement. These tween frames follow the solver's path and are safer
than straight-line interpolation across a large deformation. Tweens are
generated together with their destination frame, never as a separate earlier
generation pass.

## Browser player

Both pages use the same player. It:

- loads the canonical geometry and a frame dataset;
- verifies that their geometry versions match;
- interpolates corresponding points between frames;
- draws the resulting polygons; and
- exposes play, pause, and direct frame selection.

Gapmover selects frames by year. World Sizer selects frames by measurement.
The player contains no cartogram solver.

The shared player lives in the site's top-level `static/` directory. Project
static directories are scoped to one project and cannot provide one file to
both pages.

A dataset can use a simple structure initially:

```json
{
  "geometry": "world-v1",
  "frames": {
    "1800": [[1200, 3400], [1300, 3500]],
    "1820": [[1190, 3410], [1310, 3510]]
  }
}
```

Coordinates are scaled integers to reduce file size and avoid unnecessary
floating-point text. Frames should be delta-encoded against the previous frame
before HTTP compression. We set a download-size budget before generating new
frames and use it to decide how many solver tween frames to retain.

## Source data and reproducibility

The repository must contain or document how to obtain every input needed to
regenerate the shipped frames:

- canonical geometry source and projection settings;
- country-code mappings;
- every World Sizer measurement and its provenance;
- historical and projected population data;
- scripts that normalize the inputs; and
- the exact generator command and settings.

Generated files should not be presented as reproducible when their generator
or source data is missing.

### Measurement audit

The served World Sizer data cannot yet be reproduced from its original sources.
The obsolete CIA Factbook pipeline did not produce the served schema or country
set and has been removed. The normalized snapshot is committed and
`baseline/data_audit.json` records its coverage.

Before promising to regenerate the measurement frames, audit every menu item:

- identify its current source and date;
- decide whether it is still worth offering;
- find a maintainable source or remove it; and
- commit the normalized data and its provenance.

### Missing historical countries

Historical population data does not contain a direct value for every shape in
the present-day canonical map. Missing data must not be handled by an accidental
truthiness check or an unexplained fallback.

`data/country_mappings.json` records known code changes and the remaining legacy
continent-average fallback. Replacing the population timeline still requires a
researched rule for each historical case rather than relying on that fallback.

## Validation

Generation should fail rather than silently substitute invented values. Checks
include:

- every geometry country has an explicit value or documented missing-data rule;
- values are finite and non-negative;
- normalized shares sum to one within a stated floating-point tolerance;
- polygons do not fold or become invalid;
- shared points remain shared;
- rendered areas are within an agreed tolerance of their targets;
- every browser frame has the expected number of points.

The generator should produce a summary of area error, distortion, movement,
forward/backward differences, and validation failures for every frame.

## Implementation status

Both pages use the shared player and canonical geometry. World Sizer's
relaxation paths and Gapmover's population timeline are generated offline by
the Python solver. The opaque legacy population frames remain as a compressed
comparison baseline. Baseline hashes, numerical comparisons, data coverage,
and the one-megabyte compressed path budget are recorded in the repository.

Population years start independently from the base geometry. A short projection
pass after relaxation restores local shape templates and averages coordinates
at shared borders. This prevents distortions from accumulating across years and
removes the long folded edges previously visible around the Horn of Africa and
Southeast Asia.

The force solver can still fold Canada's outline in extreme measurement paths.
Preventing that without degrading the rest of the map requires a constrained
optimizer rather than an extra bridge or a local post-processing step.

Indonesia exposed a separate multi-shape layout problem. Newly generated paths
scale its parts around the country's center and anchor Sumatra to the southern
tip of Malaysia as a proxy for Singapore. Applying the same rule to every
multi-shape country introduced new folds, so the change remains limited to the
measured case.

The Philippines keeps its original overall layout, but island bridges remain
within the Philippine chain instead of tethering two shapes to Malaysia. This
removes the severe internal overlap seen at high population multipliers without
adding another country-specific layout scale. A bridge from China preserves
separation when China's 1800 population multiplier expands toward the islands.

The remaining work is source replacement: obtain maintained measurement and
population datasets, define every historical mapping, regenerate the frames,
and review the measured and rendered differences before replacing the legacy
snapshots. A better optimization objective is optional follow-up work.
