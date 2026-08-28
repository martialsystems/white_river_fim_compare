# Copyright (c) 2026 Martial Systems LLC

import pytest

from fimcompare.claims import require_clean, scan_text
from fimcompare.errors import ClaimBanError


def test_allowed_and_banned() -> None:
    assert scan_text("HAND bathtub vs USGS SIR 2011-5138 on the Nora window") == []
    assert "p_as_forecast" in scan_text("P(sfha | hydro) is a forecast")
    assert "hand_as_firm" in scan_text("HAND bathtub is a FIRM")
    assert "usgs_as_firm" in scan_text("USGS library polygon is a FIRM")
    assert "downtown_gage" in scan_text("gage 03353000 downtown")
    with pytest.raises(ClaimBanError):
        require_clean("site-level flood risk", source="t")
