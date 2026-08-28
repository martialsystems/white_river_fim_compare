# Copyright (c) 2026 Martial Systems LLC
"""Call sites for the refuse laws."""

from __future__ import annotations

from typing import Any

from fimforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import require_law

from fimforge.graphs.claim_bans import build_graph as build_claim_bans
from fimforge.graphs.sibling_sha import build_graph as build_sibling_sha
from fimforge.graphs.stage_gate import build_graph as build_stage_gate
from fimforge.graphs.usgs_stage import build_graph as build_usgs_stage


def require_stage(
    *,
    current_stage: str = "0",
    target_stage: str = "0",
    sibling_sha_ok: bool = False,
    usgs_stage_pinned: bool = False,
    usgs_rasterized: bool = False,
    tables_written: bool = False,
    huc_wide_wet: bool = False,
    thread_id: str = "fim_stage",
) -> None:
    require_law(
        build_stage_gate(),
        {
            "current_stage": current_stage,
            "target_stage": target_stage,
            "sibling_sha_ok": sibling_sha_ok,
            "usgs_stage_pinned": usgs_stage_pinned,
            "usgs_rasterized": usgs_rasterized,
            "tables_written": tables_written,
            "huc_wide_wet": huc_wide_wet,
        },
        allow_decisions=["allow"],
        law_id="fim.stage_gate",
        thread_id=thread_id,
        raise_error=True,
    )


def require_sibling(*, sibling_sha_ok: bool, thread_id: str = "fim_sha") -> None:
    require_law(
        build_sibling_sha(),
        {"sibling_sha_ok": sibling_sha_ok},
        allow_decisions=["allow"],
        law_id="fim.sibling_sha",
        thread_id=thread_id,
        raise_error=True,
    )


def require_usgs_stage(
    *,
    published_stage: bool,
    interpolated: bool,
    downtown_gage: bool = False,
    thread_id: str = "fim_usgs",
) -> None:
    require_law(
        build_usgs_stage(),
        {
            "published_stage": published_stage,
            "interpolated": interpolated,
            "downtown_gage": downtown_gage,
        },
        allow_decisions=["allow"],
        law_id="fim.usgs_stage",
        thread_id=thread_id,
        raise_error=True,
    )


def require_claims(**flags: Any) -> None:
    thread_id = str(flags.pop("thread_id", "fim_claims"))
    state = {
        "p_as_forecast": False,
        "hand_as_firm": False,
        "usgs_as_firm": False,
        "p_as_100yr": False,
        "site_level_flood_risk": False,
    }
    state.update(flags)
    require_law(
        build_claim_bans(),
        state,
        allow_decisions=["allow"],
        law_id="fim.claim_bans",
        thread_id=thread_id,
        raise_error=True,
    )
