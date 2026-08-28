# Copyright (c) 2026 Martial Systems LLC
"""Four-layer counts on the Nora drain-to-reach window."""

from __future__ import annotations

import numpy as np

from fimcompare.config import (
    P_DEFINITION,
    P_HEADLINE_T,
    SFHA_CODES,
    WET_NODATA,
    WET_WET,
    ZONE_UNSHADED_X,
)
from fimcompare.errors import GateError


def _iou(x: np.ndarray, y: np.ndarray) -> float:
    inter = int((x & y).sum())
    union = int((x | y).sum())
    return float(inter / union) if union else 0.0


def overlap_table(
    *,
    wet: np.ndarray,
    usgs: np.ndarray,
    zone: np.ndarray,
    p_cal: np.ndarray,
    drain_to_reach: np.ndarray,
    p_t: float = P_HEADLINE_T,
) -> dict[str, object]:
    drain = np.asarray(drain_to_reach, dtype=bool)
    if not drain.any():
        raise GateError("drain-to-reach is empty")
    if int(drain.sum()) == drain.size:
        raise GateError("C refuses a HUC-wide wet/reach mask")
    w = np.asarray(wet)
    u = np.asarray(usgs)
    z = np.asarray(zone)
    p = np.asarray(p_cal, dtype=np.float64)
    on = drain & (w != WET_NODATA) & (u != WET_NODATA)
    n = int(on.sum())
    if n == 0:
        raise GateError("no comparable cells on the reach")
    sfha = np.isin(z, list(SFHA_CODES))
    p_hi = np.isfinite(p) & (p >= float(p_t))
    hand = (w == WET_WET) & on
    lib = (u == WET_WET) & on
    a = sfha & on
    b = p_hi & on
    return {
        "p_definition": P_DEFINITION,
        "p_is_forecast": False,
        "p_headline_t": float(p_t),
        "n_reach_comparable": n,
        "n_sfha": int(a.sum()),
        "n_p_ge_t": int(b.sum()),
        "n_hand_wet": int(hand.sum()),
        "n_usgs_wet": int(lib.sum()),
        "n_hand_and_usgs": int((hand & lib).sum()),
        "n_sfha_dry_hand": int((a & ~hand).sum()),
        "n_sfha_dry_usgs": int((a & ~lib).sum()),
        "n_hand_unshaded_x": int((hand & (z == ZONE_UNSHADED_X)).sum()),
        "n_usgs_unshaded_x": int((lib & (z == ZONE_UNSHADED_X)).sum()),
        "iou_universe": "drain-to-reach",
        "iou_hand_usgs": _iou(hand, lib),
        "iou_sfha_hand": _iou(a, hand),
        "iou_sfha_usgs": _iou(a, lib),
        "iou_p_hand": _iou(b, hand),
        "iou_p_usgs": _iou(b, lib),
        "usgs_is_firm": False,
        "hand_is_firm": False,
    }


def leftover_sentence(table: dict) -> str:
    """Leftover SFHA, extra unshaded X, and USGS-in-HAND containment."""
    usgs_n = int(table["n_usgs_wet"])
    both = int(table["n_hand_and_usgs"])
    return (
        f"Leftover SFHA dry: HAND {int(table['n_sfha_dry_hand'])}, "
        f"USGS {int(table['n_sfha_dry_usgs'])}. "
        f"Unshaded X wet: HAND {int(table['n_hand_unshaded_x'])}, "
        f"USGS {int(table['n_usgs_unshaded_x'])}. "
        f"{both} of {usgs_n} USGS wet cells are HAND-wet. "
        f"IoU HAND vs USGS = {float(table['iou_hand_usgs']):.2f} on drain-to-reach."
    )
