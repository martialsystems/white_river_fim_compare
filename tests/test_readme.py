# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from fimcompare.claims import scan_text

REPO = Path(__file__).resolve().parents[1]


def test_readme_lead_and_claims() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert "03351000" in text
    assert "11.00" in text or "11 ft" in text
    assert "21.18" in text
    assert "721.5" in text
    assert "731.5" in text
    assert "indiana_flood_completion" in text
    assert "white_river_stage_inundation" in text
    assert "gitignored" in text
    assert scan_text(text) == []
    assert "—" not in text
    assert "What it is not" not in text
