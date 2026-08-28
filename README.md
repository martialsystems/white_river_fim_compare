# White River FIM compare (Nora)

This tree puts four layers on the same 5 km White River window at USGS **03351000** / NWS **NORI3** (Nora, IN). FEMA SFHA and calibrated `P(sfha | hydro) ≥ 0.75` come from the map-completion sibling. HAND wet masks at **11.00 ft** and **21.18 ft** come from the Nora stage tree. The USGS layer is the Kim 2011 2-D library (SIR **2011-5138**), served as NWS partner FIM polygons at WSE **721.5 ft** and **731.5 ft** NAVD88, the published surfaces nearest those HAND stages.

`P(sfha | hydro)` is a map-completion layer, not water at 11 ft and not water at 21.18 ft. The HAND mask is a 30 m bathtub. The USGS polygon is a calibrated FaSTMECH extent, not a FIRM.

NWS partner FIM uses zero datum 710.52 ft NAVD88. Nora uses 710.51. HAND 11.00 ft is WSE 721.51; the library surface is 721.5 (gap 0.01 ft). HAND 21.18 ft is WSE 731.69; the library surface is 731.5 (gap 0.19 ft). Scores are the Nora drain-to-reach window only. The USGS study starts at the gage and runs about 11 miles downstream toward the Indianapolis Museum of Art; the Nora window also includes 5 km upstream, so HAND is a superset.

| Quantity | Flood 11.00 ft / USGS 721.5 | Crest 21.18 ft / USGS 731.5 |
|----------|----------------------------:|----------------------------:|
| HAND wet | 1197 | 1876 |
| USGS wet | 528 | 619 |
| USGS wet also HAND | 504 of 528 | 618 of 619 |
| IoU HAND vs USGS | 0.41 | 0.33 |
| SFHA dry on HAND | 369 | 50 |
| SFHA dry on USGS | 989 | 916 |
| Unshaded X wet HAND | 38 | 338 |
| Unshaded X wet USGS | 2 | 15 |

IoU is on drain-to-reach cells only. Same window as https://github.com/martialsystems/white_river_stage_inundation.

![Figure 1. Flood stage vs USGS WSE 721.5](logs/nora_live/four_wet.png)

Figure 1. Four layers at NWS flood stage 11.00 ft and the nearest published USGS library surface (WSE 721.5 ft).

- SFHA: mapped floodway ∪ SFHA on the window.
- P ≥ 0.75: sibling map-completion, not water at 11 ft.
- HAND wet: bathtub at 11.00 ft.
- USGS: SIR 2011-5138 polygon at WSE 721.5 ft.

![Figure 2. Crest vs USGS WSE 731.5](logs/nora_live/four_wet_crest_2026-08-15.png)

Figure 2. Same four layers at the 2026-08-15 crest 21.18 ft and USGS WSE 731.5 ft.

- Extra HAND wet filled leftover SFHA (dry 369 to 50) and lit unshaded X (38 to 338).
- USGS stays tight: 618 of 619 library-wet cells are already HAND-wet. IoU 0.41 to 0.33 because HAND grows faster than the library.

Live rasters, the NWS shapefile zip, and `*.tif` stay gitignored; `logs/nora_live/four_wet.png` and `logs/nora_live/four_wet_crest_2026-08-15.png` are the committed figures.

Related trees:

- https://github.com/martialsystems/indiana_flood_completion (HUC-8 05120201 map completion; same HAND grid)
- https://github.com/martialsystems/white_river_stage_inundation (Nora HAND bathtub at 11.00 ft and 21.18 ft)

Limitations:

- 30 m HAND vs a 10 m FaSTMECH polygon, clipped to the Nora window, not the full 11-mile library reach.
- 0.01 ft and 0.19 ft WSE gaps; no interpolated USGS surface.
- Crest 21.18 ft is NWS provisional.
- One gage, two library surfaces. No third model, no whole HUC, no climate.

| File | Role |
|------|------|
| [METHODOLOGY.md](METHODOLOGY.md) | Locked contract |
| [AGENTS.md](AGENTS.md) | Agent rules |
| [CHECKLIST.md](CHECKLIST.md) | Operator list |
| `src/fimcompare/` | Stage pin, rasterize, IoU, claims |
| `fimforge/` | GraphForge pin |

## Stage 0

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
```

Hard gate: fixture IoU is on drain-to-reach, claim scan clean, product laws allow Stage 0. See METHODOLOGY.md.

Live (sibling rasters on disk, NWS zip fetched to `data/raw`):

```bash
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```
