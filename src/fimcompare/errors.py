# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class SiblingShaError(GateError):
    """Frozen sibling raster sha drifted."""


class UsgsStageError(GateError):
    """Requested USGS library stage is interpolated, off-list, or the wrong gage."""


class FetchError(RuntimeError):
    """USGS / NWS library download failed."""
