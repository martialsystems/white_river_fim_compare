# Operator checklist

1. Fixture Stage 0 green (`scripts/run_fixture.py`).
2. Indiana and Nora sibling rasters on disk; band sha matches `LOCKED_BAND_SHA256`.
3. NWS NORI3 zip in `data/raw` (fetched or copied). Stems 721_5 and 731_5 present.
4. Live `scripts/run_live.py logs/nora_live`.
5. README table matches `logs/nora_live/stage_c_report.json`.
6. Claim scan clean. No downtown Indianapolis library.
7. Push public `martialsystems/white_river_fim_compare`.
