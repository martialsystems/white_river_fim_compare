# Methodology: Nora HAND vs USGS SIR 2011-5138

Locked contract for `white_river_fim_compare`. Freeze both siblings. Do not recompute HAND. Do not train. Do not paint a HUC.

## Reach and window

USGS 03351000 White River near Nora, IN (NWS NORI3). The membership test is the Nora drain-to-reach mask from `white_river_stage_inundation` (`wet.tif` cells that are not nodata). That is a 5 km White River mainstem plus 1 km margin, EPSG:5070, 30 m, 401 by 401.

The USGS library covers about 11 miles from the Nora gage downstream toward the Indianapolis Museum of Art. This tree clips the library polygon to the Nora window. Scores are that clip only.

## Four layers

| Layer | Rule |
|-------|------|
| FEMA SFHA | Nora `zone_class.tif` codes floodway ∪ SFHA |
| Map-completion P | Nora `p_calibrated.tif` ≥ 0.75 |
| HAND wet | Nora `wet.tif` at 11.00 ft; `wet_crest_2026-08-15.tif` at 21.18 ft |
| USGS library | NWS partner FIM polygons for NORI3, Kim 2011 FaSTMECH, SIR 2011-5138 |

Published library surfaces (WSE ft NAVD88, from the NWS shapefile stems): 718.0, 718.5, then 719.5 through 732.5 by 1.0 ft. Paint only those stems. Do not interpolate a 11.00 ft or 21.18 ft USGS polygon.

Pinned pairs:

| HAND | HAND WSE | USGS WSE | Gap |
|------|---------:|---------:|----:|
| 11.00 ft | 721.51 | 721.5 | 0.01 ft |
| 21.18 ft | 731.69 | 731.5 | 0.19 ft |

NWS zeroDatum is 710.52 ft. Nora datum is 710.51 ft. Caption that 0.01 ft offset.

GIS source: `https://water.noaa.gov/resources/downloads/fim/ind/nori3/shapefile/nori3_shapefiles.zip`. Metadata cites SIR 2011-5138 and USGS Indiana Water Science Center. Partner FIM is the hydraulic library, not NWM HAND.

## Physics (siblings, not this tree)

Nora wet iff D8 drain-to-reach and finite HAND and `HAND < Δ`, `Δ = WSE − h_channel`. `h_channel` is sibling DEM at the White River cell, not gage zero. This tree does not repaint that mask.

## Overlap

Universe: drain-to-reach. HAND-nodata stays out. Headline IoU is HAND vs USGS. Also leftover SFHA (mapped SFHA, dry on that layer) and extra unshaded Zone X (wet on that layer). Descriptive IoU of SFHA and of P ≥ 0.75 against each inundation layer. No PR-AUC. No retraining.

## Stages

0: sibling sha, published WSE pin, fixture path.
A: reproject 721_5 and 731_5 to EPSG:5070, rasterize to the Nora window, clip drain-to-reach.
B: overlap tables.
C: two 2×2 figures, claim scan.

Do not skip. A refuses a missing library polygon. C refuses a HUC-wide mask.

## Claims

Allowed: HAND bathtub vs USGS SIR 2011-5138 on the Nora window; nearest published WSE 721.5 / 731.5; mapped SFHA; calibrated P as a map layer; IoU / leftover-SFHA / extra unshaded X on drain-to-reach.

Banned: 100-year exceedance; P as a forecast; HAND as a FIRM; USGS library as a FIRM; site-level flood risk; casualty / climate / population-at-risk; training on FEMA; whole-HUC paint; downtown Indianapolis library.

## Freeze

Indiana band sha256 for `p_sfha_calibrated` and `zone_class` as in Nora `LOCKED_BAND_SHA256`. Nora live wet masks stay on disk. Do not rewrite Nora `three_wet.png`.
