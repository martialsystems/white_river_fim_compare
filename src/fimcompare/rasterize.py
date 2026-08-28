# Copyright (c) 2026 Martial Systems LLC
"""Reproject a NORI3 library polygon onto the Nora 30 m window."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from fimcompare.config import TEMPLATE_CRS, USGS_POLY_DIR, WET_NODATA
from fimcompare.errors import GateError, UsgsStageError
from fimcompare.usgs import require_published_wse, wse_to_stem


def polygon_path(extract_root: Path, wse_ft: float) -> Path:
    stem = wse_to_stem(require_published_wse(wse_ft))
    path = extract_root / USGS_POLY_DIR / f"{stem}.shp"
    if not path.is_file():
        nested = extract_root / "shp" / "ahps" / "inundation" / "nori3" / "polygons" / f"{stem}.shp"
        if nested.is_file():
            return nested
        raise UsgsStageError(f"library polygon missing: {path}")
    return path


def rasterize_polygon(
    shp: Path,
    *,
    transform,
    height: int,
    width: int,
    drain: np.ndarray,
) -> np.ndarray:
    import fiona
    from rasterio.features import rasterize
    from rasterio.warp import transform_geom

    if not shp.is_file():
        raise UsgsStageError(f"library polygon missing: {shp}")
    geoms: list = []
    with fiona.open(shp) as src:
        src_crs = src.crs
        if src_crs is None:
            src_crs = "EPSG:4269"
        for feat in src:
            geom = feat.get("geometry")
            if not geom:
                continue
            geoms.append(
                transform_geom(src_crs, f"EPSG:{TEMPLATE_CRS}", geom, precision=6)
            )
    if not geoms:
        raise GateError(f"no geometries in {shp}")
    arr = rasterize(
        ((g, 1) for g in geoms),
        out_shape=(int(height), int(width)),
        transform=transform,
        fill=0,
        dtype="uint8",
        all_touched=False,
    )
    mask = np.asarray(drain, dtype=bool)
    if arr.shape != mask.shape:
        raise GateError(f"rasterize shape {arr.shape} != drain {mask.shape}")
    out = np.where(mask, arr, WET_NODATA).astype(np.uint8)
    return out
