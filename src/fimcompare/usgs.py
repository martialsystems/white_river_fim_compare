# Copyright (c) 2026 Martial Systems LLC
"""Pin SIR 2011-5138 library stages. No interpolation. Refuse downtown 03353000."""

from __future__ import annotations

from fimcompare.config import (
    GAGE_ID,
    PUBLISHED_WSE_FT,
    REFUSED_GAGE_ID,
    REFUSED_SIR,
    USGS_CREST_WSE_FT,
    USGS_FLOOD_WSE_FT,
)
from fimcompare.errors import UsgsStageError


def wse_to_stem(wse_ft: float) -> str:
    whole, frac = divmod(round(float(wse_ft) * 10), 10)
    return f"{int(whole)}_{int(frac)}"


def nearest_published_wse(wse_ft: float) -> float:
    target = float(wse_ft)
    return min(PUBLISHED_WSE_FT, key=lambda x: abs(x - target))


def require_published_wse(wse_ft: float) -> float:
    w = float(wse_ft)
    for pub in PUBLISHED_WSE_FT:
        if abs(w - pub) < 1e-9:
            return pub
    raise UsgsStageError(
        f"WSE {w} ft is not a published SIR 2011-5138 / NORI3 library surface "
        f"{PUBLISHED_WSE_FT}. Do not interpolate."
    )


def require_nora_gage(gage_id: str) -> str:
    gid = str(gage_id)
    if gid == REFUSED_GAGE_ID:
        raise UsgsStageError(
            f"gage {gid} is downtown Indianapolis SIR {REFUSED_SIR}, not Nora"
        )
    if gid != GAGE_ID:
        raise UsgsStageError(f"gage {gid} is not {GAGE_ID}")
    return gid


def pin_pairs() -> dict[str, dict[str, float]]:
    """HAND flood/crest WSE → nearest published USGS library WSE."""
    flood = require_published_wse(USGS_FLOOD_WSE_FT)
    crest = require_published_wse(USGS_CREST_WSE_FT)
    return {
        "flood": {
            "hand_stage_ft": 11.0,
            "hand_wse_ft": 721.51,
            "usgs_wse_ft": flood,
            "gap_ft": round(721.51 - flood, 2),
        },
        "crest": {
            "hand_stage_ft": 21.18,
            "hand_wse_ft": 731.69,
            "usgs_wse_ft": crest,
            "gap_ft": round(731.69 - crest, 2),
        },
    }
