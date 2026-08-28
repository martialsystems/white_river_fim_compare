# Agent notes: white_river_fim_compare

Public GitHub. MIT on this snapshot. Geography is USGS 03351000 Nora on HUC-8 05120201. Siblings https://github.com/martialsystems/indiana_flood_completion and https://github.com/martialsystems/white_river_stage_inundation are frozen. Do not edit them. Do not recompute HAND. Do not add a second HUC, a third model, or a water-treatment overlay.

## Product

Four layers on the Nora drain-to-reach window: FEMA SFHA, P ≥ 0.75, HAND wet at 11.00 ft and 21.18 ft, USGS SIR 2011-5138 polygon at WSE 721.5 and 731.5. Lead with containment (N of M USGS-wet also HAND-wet, plus miss). IoU stays in that same paragraph as the superset / upstream-window reason. Combined interview sheet is not in git. WTP/substations is a different folder.

## Stages

0, A, B, C. `fimforge.gate.require_stage` refuses skips. A refuses an unpublished USGS WSE. C refuses a HUC-wide mask.

## Claims

Run `fimcompare.claims.scan_text` on reports, README, and figure titles. Fail closed on 100-year exceedance, P as a forecast, HAND as a FIRM, USGS library as a FIRM, site-level flood risk, downtown Indianapolis library.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs `.venv/bin/python -m pytest`, `scripts/run_fixture.py`, and `fimforge/scripts/sanity_fimforge.py`. Do not use stock `/usr/bin/python3 -m pytest`: it has no rasterio and dies in collection.

## GraphForge

Pin is `fimforge/`. Engine checkout `~/graphforge`. No catalog/`surfaces.json` unless the operator asks.
