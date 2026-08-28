# Copyright (c) 2026 Martial Systems LLC

import pytest

from fimcompare.config import GAGE_ID, USGS_CREST_WSE_FT, USGS_FLOOD_WSE_FT
from fimcompare.errors import UsgsStageError
from fimcompare.usgs import (
    nearest_published_wse,
    pin_pairs,
    require_nora_gage,
    require_published_wse,
    wse_to_stem,
)


def test_published_wse_and_stems() -> None:
    assert require_published_wse(721.5) == 721.5
    assert require_published_wse(731.5) == 731.5
    assert wse_to_stem(721.5) == "721_5"
    assert wse_to_stem(731.5) == "731_5"
    with pytest.raises(UsgsStageError):
        require_published_wse(721.51)
    with pytest.raises(UsgsStageError):
        require_published_wse(11.0)


def test_nearest_is_not_used_as_paint() -> None:
    assert nearest_published_wse(721.51) == USGS_FLOOD_WSE_FT
    assert nearest_published_wse(731.69) == USGS_CREST_WSE_FT
    pairs = pin_pairs()
    assert pairs["flood"]["usgs_wse_ft"] == 721.5
    assert pairs["crest"]["usgs_wse_ft"] == 731.5
    assert pairs["flood"]["gap_ft"] == 0.01
    assert pairs["crest"]["gap_ft"] == 0.19


def test_refuse_downtown_gage() -> None:
    assert require_nora_gage(GAGE_ID) == GAGE_ID
    with pytest.raises(UsgsStageError):
        require_nora_gage("03353000")
    with pytest.raises(UsgsStageError):
        require_nora_gage("03349000")
