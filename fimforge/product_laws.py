# Copyright (c) 2026 Martial Systems LLC
"""Four refuse laws: sha, USGS stage pin, claims, stage gate. VBD is the finish gate."""

from __future__ import annotations

from typing import Any


def laws() -> list[dict[str, Any]]:
    from fimforge.graphs.claim_bans import build_graph as claim_bans
    from fimforge.graphs.sibling_sha import build_graph as sibling_sha
    from fimforge.graphs.stage_gate import build_graph as stage_gate
    from fimforge.graphs.usgs_stage import build_graph as usgs_stage

    return [
        {
            "id": "fim.stage_gate",
            "build": stage_gate,
            "state": {
                "current_stage": "0",
                "target_stage": "0",
                "sibling_sha_ok": True,
                "usgs_stage_pinned": False,
                "usgs_rasterized": False,
                "tables_written": False,
                "huc_wide_wet": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "fim.sibling_sha",
            "build": sibling_sha,
            "state": {"sibling_sha_ok": True},
            "allow_decisions": ["allow"],
        },
        {
            "id": "fim.usgs_stage",
            "build": usgs_stage,
            "state": {
                "published_stage": True,
                "interpolated": False,
                "downtown_gage": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "fim.claim_bans",
            "build": claim_bans,
            "state": {
                "p_as_forecast": False,
                "hand_as_firm": False,
                "usgs_as_firm": False,
                "p_as_100yr": False,
                "site_level_flood_risk": False,
            },
            "allow_decisions": ["allow"],
        },
    ]
