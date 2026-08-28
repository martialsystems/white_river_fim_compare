# Copyright (c) 2026 Martial Systems LLC
"""Tiny 16x16 window so CI scores without a live USGS download."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from fimcompare.config import (
    FIXTURE_COLS,
    FIXTURE_NORTH,
    FIXTURE_ROWS,
    FIXTURE_WEST,
    TEMPLATE_CRS,
    TEMPLATE_RES_M,
    WET_DRY,
    WET_NODATA,
    WET_WET,
    ZONE_SFHA,
    ZONE_UNSHADED_X,
)


def affine():
    from rasterio.transform import from_origin

    return from_origin(FIXTURE_WEST, FIXTURE_NORTH, TEMPLATE_RES_M, TEMPLATE_RES_M)


def arrays() -> dict[str, np.ndarray]:
    rows, cols = FIXTURE_ROWS, FIXTURE_COLS
    drain = np.zeros((rows, cols), dtype=bool)
    drain[2:14, 2:10] = True
    wet = np.full((rows, cols), WET_NODATA, dtype=np.uint8)
    usgs = np.full((rows, cols), WET_NODATA, dtype=np.uint8)
    zone = np.zeros((rows, cols), dtype=np.uint8)
    p = np.full((rows, cols), np.nan, dtype=np.float64)
    wet[drain] = WET_DRY
    usgs[drain] = WET_DRY
    # Channel: both wet. Left bank: HAND wet, USGS dry, SFHA leftover.
    # Right bank: USGS wet into unshaded X.
    wet[4:12, 4:7] = WET_WET
    usgs[4:12, 5:9] = WET_WET
    zone[drain] = ZONE_UNSHADED_X
    zone[4:12, 3:7] = ZONE_SFHA
    p[drain] = 0.2
    p[4:12, 4:8] = 0.82
    return {"wet": wet, "usgs": usgs, "zone": zone, "p": p, "drain": drain}


def write_geojson(dest: Path) -> Path:
    """A square in lon/lat covering the fixture Albers window enough to rasterize."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        '{"type":"FeatureCollection","features":[{"type":"Feature","properties":'
        '{"Id":1},"geometry":{"type":"Polygon","coordinates":'
        "[[[-86.12,39.90],[-86.11,39.90],[-86.11,39.91],[-86.12,39.91],[-86.12,39.90]]]}}]}",
        encoding="utf-8",
    )
    return dest


def write_profile() -> dict:
    return {
        "driver": "GTiff",
        "height": FIXTURE_ROWS,
        "width": FIXTURE_COLS,
        "count": 1,
        "dtype": "uint8",
        "crs": f"EPSG:{TEMPLATE_CRS}",
        "transform": affine(),
        "nodata": WET_NODATA,
    }
