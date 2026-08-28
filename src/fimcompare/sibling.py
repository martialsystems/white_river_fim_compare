# Copyright (c) 2026 Martial Systems LLC
"""Read-only sibling rasters. Refuse if indiana bands or Nora wet masks drift."""

from __future__ import annotations

import hashlib
from pathlib import Path

from fimcompare.config import (
    INDIANA_DEFAULT,
    LOCKED_BAND_SHA256,
    LOCKED_TRANSFORM_SHA256,
    NORA_P,
    NORA_WET,
    NORA_WET_CREST,
    NORA_ZONE,
)
from fimcompare.errors import SiblingShaError


def transform_sha256_from_raster(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        t = src.transform
        payload = (
            f"{int(src.crs.to_epsg() or 0)}|{src.width}|{src.height}|"
            f"{t.a},{t.b},{t.c},{t.d},{t.e},{t.f}"
        )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def band_sha256_from_raster(path: Path) -> str:
    import rasterio

    with rasterio.open(path) as src:
        return hashlib.sha256(src.read(1).tobytes()).hexdigest()


def require_band_sha(path: Path, *, expected: str) -> str:
    if not path.is_file():
        raise SiblingShaError(f"sibling raster missing: {path}")
    got = band_sha256_from_raster(path)
    if got != expected:
        raise SiblingShaError(f"band {got} != locked {expected} ({path})")
    return got


def indiana_paths(root: Path | None = None) -> dict[str, Path]:
    base = Path(root) if root is not None else INDIANA_DEFAULT
    interim = base / "data" / "interim"
    return {
        "p_calibrated": interim / "p_sfha_calibrated.tif",
        "zone_class": interim / "zone_class.tif",
        "hand": interim / "hand.tif",
    }


def nora_paths() -> dict[str, Path]:
    return {
        "wet": NORA_WET,
        "wet_crest": NORA_WET_CREST,
        "zone_class": NORA_ZONE,
        "p_calibrated": NORA_P,
    }


def require_indiana_bands(root: Path | None = None) -> dict[str, str]:
    paths = indiana_paths(root)
    out: dict[str, str] = {}
    for key, expected in LOCKED_BAND_SHA256.items():
        out[key] = require_band_sha(paths[key], expected=expected)
    return out


def require_nora_window(wet_path: Path = NORA_WET) -> str:
    if not wet_path.is_file():
        raise SiblingShaError(f"Nora wet mask missing: {wet_path}")
    got = transform_sha256_from_raster(wet_path)
    # Live Nora is a crop of the HUC template: same 30 m / 5070, not the HUC-wide sha.
    import rasterio

    with rasterio.open(wet_path) as src:
        if int(src.crs.to_epsg() or 0) != 5070:
            raise SiblingShaError(f"Nora wet CRS {src.crs} is not EPSG:5070")
        if abs(src.transform.a - 30.0) > 1e-6 or abs(src.transform.e + 30.0) > 1e-6:
            raise SiblingShaError(f"Nora wet cell size is not 30 m: {src.transform}")
    return got


def require_live_siblings(*, indiana_root: Path | None = None) -> dict[str, str]:
    bands = require_indiana_bands(indiana_root)
    nora = nora_paths()
    for key in ("wet", "wet_crest", "zone_class", "p_calibrated"):
        if not nora[key].is_file():
            raise SiblingShaError(f"Nora raster missing: {nora[key]}")
    require_nora_window(nora["wet"])
    bands["nora_wet_transform"] = transform_sha256_from_raster(nora["wet"])
    bands["indiana_transform"] = LOCKED_TRANSFORM_SHA256
    return bands
