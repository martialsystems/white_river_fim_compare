# Copyright (c) 2026 Martial Systems LLC

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from fimforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError

from fimforge.gate import require_claims, require_sibling, require_stage, require_usgs_stage
from fimforge.product_laws import laws


def test_stage_gate_allows_zero() -> None:
    require_stage(current_stage="0", target_stage="0", thread_id="t.s0")


def test_stage_gate_blocks_skip_and_rasterize_without_pin() -> None:
    with pytest.raises(LawBlockedError):
        require_stage(
            current_stage="0",
            target_stage="B",
            sibling_sha_ok=True,
            usgs_stage_pinned=True,
            thread_id="t.skip",
        )
    with pytest.raises(LawBlockedError):
        require_stage(
            current_stage="0",
            target_stage="A",
            sibling_sha_ok=True,
            usgs_stage_pinned=False,
            thread_id="t.nopin",
        )


def test_sibling_and_usgs_laws() -> None:
    require_sibling(sibling_sha_ok=True, thread_id="t.sha.ok")
    with pytest.raises(LawBlockedError):
        require_sibling(sibling_sha_ok=False, thread_id="t.sha.bad")
    require_usgs_stage(
        published_stage=True, interpolated=False, downtown_gage=False, thread_id="t.u.ok"
    )
    with pytest.raises(LawBlockedError):
        require_usgs_stage(
            published_stage=True, interpolated=True, downtown_gage=False, thread_id="t.u.int"
        )
    with pytest.raises(LawBlockedError):
        require_usgs_stage(
            published_stage=True, interpolated=False, downtown_gage=True, thread_id="t.u.dt"
        )


def test_claim_bans() -> None:
    require_claims(thread_id="t.c.ok")
    with pytest.raises(LawBlockedError):
        require_claims(p_as_forecast=True, thread_id="t.c.p")
    with pytest.raises(LawBlockedError):
        require_claims(usgs_as_firm=True, thread_id="t.c.u")


def test_laws_registry() -> None:
    ids = {row["id"] for row in laws()}
    assert ids == {
        "fim.stage_gate",
        "fim.sibling_sha",
        "fim.usgs_stage",
        "fim.claim_bans",
    }
