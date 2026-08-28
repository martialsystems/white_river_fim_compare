# Copyright (c) 2026 Martial Systems LLC
"""Fetch the NWS-hosted NORI3 shapefile zip (Kim 2011 library)."""

from __future__ import annotations

import urllib.request
from pathlib import Path
from zipfile import ZipFile

from fimcompare.config import USGS_ZIP_NAME, USGS_ZIP_URL, USER_AGENT
from fimcompare.errors import FetchError


def fetch_zip(dest_dir: Path, *, url: str = USGS_ZIP_URL) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / USGS_ZIP_NAME
    if dest.is_file() and dest.stat().st_size > 1_000_000:
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            dest.write_bytes(resp.read())
    except Exception as exc:  # noqa: BLE001
        raise FetchError(f"USGS/NWS library download failed: {url}: {exc}") from exc
    if dest.stat().st_size < 1_000_000:
        raise FetchError(f"library zip too small ({dest.stat().st_size} bytes): {url}")
    return dest


def extract_zip(zip_path: Path, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    with ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
    return dest_dir
