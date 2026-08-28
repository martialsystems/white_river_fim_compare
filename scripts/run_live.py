#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Live Nora window vs SIR 2011-5138. Needs sibling rasters and the NWS zip."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from fimcompare.pipeline import run_live  # noqa: E402


def main() -> int:
    log_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "logs" / "nora_live"
    raw = REPO / "data" / "raw"
    report = run_live(log_dir, raw_dir=raw)
    print(report["flood"]["leftover"])
    print(report["crest"]["leftover"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
