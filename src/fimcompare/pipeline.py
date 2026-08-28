# Copyright (c) 2026 Martial Systems LLC
"""Stages 0, A, B, C. Do not skip."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from fimcompare.claims import require_clean, require_paths_clean
from fimcompare.compare import leftover_sentence, overlap_table
from fimcompare.config import (
    GAGE_ID,
    HAND_CREST_STAGE_FT,
    HAND_FLOOD_STAGE_FT,
    NORA_P,
    NORA_WET,
    NORA_WET_CREST,
    NORA_ZONE,
    SIR,
    USGS_CREST_WSE_FT,
    USGS_FLOOD_WSE_FT,
    WET_NODATA,
)
from fimcompare.errors import GateError
from fimcompare.figure import crest_copy, flood_copy, write_four_panel
from fimcompare.fixture import arrays as fixture_arrays
from fimcompare.http import extract_zip, fetch_zip
from fimcompare.rasterize import polygon_path, rasterize_polygon
from fimcompare.sibling import nora_paths, require_live_siblings
from fimcompare.usgs import pin_pairs, require_nora_gage, require_published_wse

try:
    from fimforge.gate import require_claims, require_sibling, require_stage, require_usgs_stage
except ImportError:  # pragma: no cover: fixture tests import pipeline without GraphForge.
    def require_claims(**kwargs):  # type: ignore[no-redef]
        del kwargs

    def require_sibling(**kwargs):  # type: ignore[no-redef]
        del kwargs

    def require_stage(**kwargs):  # type: ignore[no-redef]
        del kwargs

    def require_usgs_stage(**kwargs):  # type: ignore[no-redef]
        del kwargs


def _drain_from_wet(wet: np.ndarray) -> np.ndarray:
    return np.asarray(wet) != WET_NODATA


def _read(path: Path):
    import rasterio

    with rasterio.open(path) as src:
        return src.read(1), src.profile.copy()


def stage0_fixture(log_dir: Path) -> dict:
    require_nora_gage(GAGE_ID)
    require_published_wse(USGS_FLOOD_WSE_FT)
    require_published_wse(USGS_CREST_WSE_FT)
    require_stage(
        current_stage="0",
        target_stage="0",
        sibling_sha_ok=True,
        usgs_stage_pinned=True,
        thread_id="fixture.s0",
    )
    require_sibling(sibling_sha_ok=True, thread_id="fixture.sha")
    require_usgs_stage(
        published_stage=True,
        interpolated=False,
        downtown_gage=False,
        thread_id="fixture.usgs",
    )
    require_claims(thread_id="fixture.claims")
    blobs = fixture_arrays()
    table = overlap_table(
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
    )
    sentence = leftover_sentence(table)
    require_clean(sentence, source="fixture_sentence")
    log_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": "0",
        "gage_id": GAGE_ID,
        "sir": SIR,
        "fixture": True,
        "p_is_forecast": False,
        "hand_is_firm": False,
        "usgs_is_firm": False,
        "pairs": pin_pairs(),
        "table": table,
        "leftover": sentence,
    }
    (log_dir / "stage0_report.json").write_text(json.dumps(report, indent=2) + "\n")
    title, sub, footer, hand_c, usgs_c = flood_copy(
        iou=float(table["iou_hand_usgs"]), leftover=sentence
    )
    write_four_panel(
        log_dir / "four_wet.png",
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
        title=title,
        subtitle=sub,
        footer=footer,
        hand_caption=hand_c,
        usgs_caption=usgs_c,
    )
    require_paths_clean([log_dir / "stage0_report.json"])
    return report


def run_live(log_dir: Path, *, raw_dir: Path) -> dict:
    require_nora_gage(GAGE_ID)
    bands = require_live_siblings()
    require_sibling(sibling_sha_ok=True, thread_id="live.sha")
    require_usgs_stage(
        published_stage=True,
        interpolated=False,
        downtown_gage=False,
        thread_id="live.usgs",
    )
    require_stage(
        current_stage="0",
        target_stage="A",
        sibling_sha_ok=True,
        usgs_stage_pinned=True,
        thread_id="live.sA",
    )
    zip_path = fetch_zip(raw_dir)
    extract_root = raw_dir / "extracted"
    extract_zip(zip_path, extract_root)
    wet, profile = _read(NORA_WET)
    wet_crest, _ = _read(NORA_WET_CREST)
    zone, _ = _read(NORA_ZONE)
    p_cal, _ = _read(NORA_P)
    drain = _drain_from_wet(wet)
    transform = profile["transform"]
    h, w = wet.shape
    flood_shp = polygon_path(extract_root, USGS_FLOOD_WSE_FT)
    crest_shp = polygon_path(extract_root, USGS_CREST_WSE_FT)
    usgs_flood = rasterize_polygon(flood_shp, transform=transform, height=h, width=w, drain=drain)
    usgs_crest = rasterize_polygon(crest_shp, transform=transform, height=h, width=w, drain=drain)
    rasters = log_dir / "rasters"
    rasters.mkdir(parents=True, exist_ok=True)
    _write_uint8(rasters / "usgs_721_5.tif", usgs_flood, profile)
    _write_uint8(rasters / "usgs_731_5.tif", usgs_crest, profile)
    require_stage(
        current_stage="A",
        target_stage="B",
        sibling_sha_ok=True,
        usgs_stage_pinned=True,
        usgs_rasterized=True,
        thread_id="live.sB",
    )
    flood_table = overlap_table(
        wet=wet, usgs=usgs_flood, zone=zone, p_cal=p_cal, drain_to_reach=drain
    )
    crest_table = overlap_table(
        wet=wet_crest, usgs=usgs_crest, zone=zone, p_cal=p_cal, drain_to_reach=drain
    )
    flood_sent = leftover_sentence(flood_table)
    crest_sent = leftover_sentence(crest_table)
    require_clean(flood_sent, source="live_flood_sentence")
    require_clean(crest_sent, source="live_crest_sentence")
    require_stage(
        current_stage="B",
        target_stage="C",
        sibling_sha_ok=True,
        usgs_stage_pinned=True,
        usgs_rasterized=True,
        tables_written=True,
        huc_wide_wet=False,
        thread_id="live.sC",
    )
    t1, s1, f1, h1, u1 = flood_copy(
        iou=float(flood_table["iou_hand_usgs"]), leftover=flood_sent
    )
    write_four_panel(
        log_dir / "four_wet.png",
        wet=wet,
        usgs=usgs_flood,
        zone=zone,
        p_cal=p_cal,
        drain_to_reach=drain,
        title=t1,
        subtitle=s1,
        footer=f1,
        hand_caption=h1,
        usgs_caption=u1,
    )
    t2, s2, f2, h2, u2 = crest_copy(leftover=crest_sent)
    write_four_panel(
        log_dir / "four_wet_crest_2026-08-15.png",
        wet=wet_crest,
        usgs=usgs_crest,
        zone=zone,
        p_cal=p_cal,
        drain_to_reach=drain,
        title=t2,
        subtitle=s2,
        footer=f2,
        hand_caption=h2,
        usgs_caption=u2,
    )
    report = {
        "stage": "C",
        "gage_id": GAGE_ID,
        "sir": SIR,
        "fixture": False,
        "p_is_forecast": False,
        "hand_is_firm": False,
        "usgs_is_firm": False,
        "hand_flood_stage_ft": HAND_FLOOD_STAGE_FT,
        "hand_crest_stage_ft": HAND_CREST_STAGE_FT,
        "pairs": pin_pairs(),
        "sibling_sha": bands,
        "nora_paths": {k: v.name for k, v in nora_paths().items()},
        "flood": {"table": flood_table, "leftover": flood_sent},
        "crest": {"table": crest_table, "leftover": crest_sent},
    }
    (log_dir / "stage_c_report.json").write_text(json.dumps(report, indent=2) + "\n")
    require_paths_clean(
        [
            log_dir / "stage_c_report.json",
            Path(__file__).resolve().parents[2] / "README.md",
        ]
    )
    require_claims(thread_id="live.claims")
    return report


def _write_uint8(path: Path, arr: np.ndarray, profile: dict) -> None:
    import rasterio

    prof = dict(profile)
    prof.update(count=1, dtype="uint8", nodata=WET_NODATA, compress="lzw")
    with rasterio.open(path, "w", **prof) as dst:
        dst.write(np.asarray(arr, dtype=np.uint8), 1)
