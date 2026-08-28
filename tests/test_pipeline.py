# Copyright (c) 2026 Martial Systems LLC

from pathlib import Path

from fimcompare.pipeline import stage0_fixture


def test_fixture_stage0(tmp_path: Path) -> None:
    report = stage0_fixture(tmp_path)
    assert report["gage_id"] == "03351000"
    assert report["sir"] == "2011-5138"
    assert report["p_is_forecast"] is False
    assert (tmp_path / "four_wet.png").is_file()
    assert (tmp_path / "stage0_report.json").is_file()
