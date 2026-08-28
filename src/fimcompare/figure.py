# Copyright (c) 2026 Martial Systems LLC
"""2x2: SFHA, P>=0.75, HAND wet, USGS library on the Nora window."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from fimcompare.claims import require_clean
from fimcompare.config import (
    GAGE_ID,
    P_DEFINITION,
    P_HEADLINE_T,
    SFHA_CODES,
    SIR,
    WET_WET,
)
from fimcompare.errors import GateError


def write_four_panel(
    dest: Path,
    *,
    wet: np.ndarray,
    usgs: np.ndarray,
    zone: np.ndarray,
    p_cal: np.ndarray,
    drain_to_reach: np.ndarray,
    title: str,
    subtitle: str,
    footer: str,
    hand_caption: str,
    usgs_caption: str,
) -> Path:
    require_clean(title, source="figure_title")
    require_clean(subtitle, source="figure_subtitle")
    require_clean(footer, source="figure_footer")
    require_clean(hand_caption, source="figure_hand")
    require_clean(usgs_caption, source="figure_usgs")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    drain = np.asarray(drain_to_reach, dtype=bool)
    if not drain.any() or int(drain.sum()) == drain.size:
        raise GateError("figure refuses a HUC-wide reach mask")
    sfha = np.isin(zone, list(SFHA_CODES)).astype(float)
    p = np.asarray(p_cal, dtype=np.float64)
    p_hi = np.where(np.isfinite(p) & (p >= P_HEADLINE_T), 1.0, 0.0)
    hand = (np.asarray(wet) == WET_WET).astype(float)
    lib = (np.asarray(usgs) == WET_WET).astype(float)
    for arr in (sfha, p_hi, hand, lib):
        arr[~drain] = np.nan
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 9.2))
    panels = (
        (axes[0, 0], sfha, "FEMA SFHA: floodway ∪ SFHA", "viridis"),
        (
            axes[0, 1],
            p_hi,
            f"{P_DEFINITION} ≥ {P_HEADLINE_T}: map-completion",
            "plasma",
        ),
        (axes[1, 0], hand, hand_caption, "cividis"),
        (axes[1, 1], lib, usgs_caption, "cividis"),
    )
    for ax, data, lab, cmap in panels:
        require_clean(lab, source="figure_panel")
        ax.imshow(data, origin="upper", cmap=cmap, vmin=0.0, vmax=1.0)
        ax.set_title(lab, fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle(title, fontsize=11)
    fig.text(0.5, 0.905, subtitle, ha="center", fontsize=8)
    fig.subplots_adjust(bottom=0.14, top=0.85, hspace=0.18, wspace=0.08)
    fig.text(0.5, 0.055, footer, ha="center", fontsize=7)
    fig.text(0.5, 0.02, f"SIR {SIR}. Not a FIRM.", ha="center", fontsize=7.5)
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, dpi=120)
    plt.close(fig)
    return dest


def flood_copy(*, iou: float, leftover: str) -> tuple[str, str, str, str, str]:
    title = f"{GAGE_ID} Nora window: HAND 11.00 ft vs USGS SIR {SIR} WSE 721.5 ft"
    subtitle = (
        "Same 5 km drain-to-reach. USGS is the Kim 2011 2-D library, not a FIRM. "
        "P is map-completion, not water at 11 ft."
    )
    footer = leftover
    hand_cap = "HAND wet: bathtub at NWS flood stage 11.00 ft"
    usgs_cap = "USGS library polygon at WSE 721.5 ft NAVD88"
    require_clean(title, source="flood_title")
    return title, subtitle, footer, hand_cap, usgs_cap


def crest_copy(*, leftover: str) -> tuple[str, str, str, str, str]:
    title = f"{GAGE_ID} Nora window: HAND 21.18 ft vs USGS SIR {SIR} WSE 731.5 ft"
    subtitle = (
        "Same window as flood stage. USGS WSE 731.5 is the published library surface "
        "nearest the 2026-08-15 crest WSE 731.69 ft."
    )
    footer = leftover
    hand_cap = "HAND wet: bathtub at crest 21.18 ft (2026-08-15)"
    usgs_cap = "USGS library polygon at WSE 731.5 ft NAVD88"
    require_clean(title, source="crest_title")
    return title, subtitle, footer, hand_cap, usgs_cap
