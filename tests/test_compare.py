# Copyright (c) 2026 Martial Systems LLC

import numpy as np
import pytest

from fimcompare.compare import leftover_sentence, overlap_table
from fimcompare.config import ZONE_SFHA, ZONE_UNSHADED_X
from fimcompare.errors import GateError
from fimcompare.fixture import arrays


def test_overlap_counts_and_refuses_huc_wide() -> None:
    blobs = arrays()
    t = overlap_table(
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
    )
    assert t["p_is_forecast"] is False
    assert t["usgs_is_firm"] is False
    assert t["iou_universe"] == "drain-to-reach"
    assert int(t["n_hand_wet"]) > 0
    assert int(t["n_usgs_wet"]) > 0
    assert int(t["n_hand_and_usgs"]) > 0
    s = leftover_sentence(t)
    assert "USGS wet cells are HAND-wet" in s
    assert "miss" in s
    assert s.index("USGS wet cells are HAND-wet") < s.index("Leftover SFHA")
    assert "Unshaded X" in s
    assert "drain-to-reach" in s
    with pytest.raises(GateError):
        overlap_table(
            wet=blobs["wet"],
            usgs=blobs["usgs"],
            zone=blobs["zone"],
            p_cal=blobs["p"],
            drain_to_reach=np.ones(blobs["wet"].shape, dtype=bool),
        )


def test_hand_and_usgs_disagree_on_fixture_bank() -> None:
    blobs = arrays()
    t = overlap_table(
        wet=blobs["wet"],
        usgs=blobs["usgs"],
        zone=blobs["zone"],
        p_cal=blobs["p"],
        drain_to_reach=blobs["drain"],
    )
    assert int(t["n_hand_wet"]) != int(t["n_usgs_wet"])
    assert float(t["iou_hand_usgs"]) < 1.0
