# Copyright (c) 2026 Martial Systems LLC
"""Refuse interpolated USGS stages and the downtown 03353000 library."""

from __future__ import annotations

from typing import Any

from fimforge._bootstrap import ensure_paths

ensure_paths()

from graphforge import END, START, StateGraph, last_value, operator_add
from graphforge.state import ChannelSpec, StateSchema


def _schema() -> StateSchema:
    return StateSchema.from_specs(
        [
            ChannelSpec("published_stage", last_value, default=False),
            ChannelSpec("interpolated", last_value, default=True),
            ChannelSpec("downtown_gage", last_value, default=False),
            ChannelSpec("violations", last_value, default=[]),
            ChannelSpec("decision", last_value, default=None),
            ChannelSpec("events", operator_add, default=[]),
        ]
    )


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    violations: list[str] = []
    if not bool(state.get("published_stage")):
        violations.append("usgs_stage_not_published")
    if bool(state.get("interpolated")):
        violations.append("usgs_stage_interpolated")
    if bool(state.get("downtown_gage")):
        violations.append("usgs_downtown_03353000")
    return {
        "violations": violations,
        "events": [
            {"node": "evaluate", "ok": len(violations) == 0, "violations": list(violations)}
        ],
    }


def build_graph() -> StateGraph:
    g = StateGraph(_schema(), name="fim.usgs_stage")

    def allow(state: dict[str, Any]) -> dict[str, Any]:
        del state
        return {"decision": "allow", "events": [{"node": "allow"}]}

    def block(state: dict[str, Any]) -> dict[str, Any]:
        return {
            "decision": "block",
            "events": [{"node": "block", "violations": state.get("violations") or []}],
        }

    def route(state: dict[str, Any]) -> str:
        return "ok" if not (state.get("violations") or []) else "bad"

    g.add_node("evaluate", _evaluate)
    g.add_node("allow", allow)
    g.add_node("block", block)
    g.add_edge(START, "evaluate")
    g.add_conditional_edges("evaluate", route, {"ok": "allow", "bad": "block"})
    g.add_edge("allow", END)
    g.add_edge("block", END)
    return g
