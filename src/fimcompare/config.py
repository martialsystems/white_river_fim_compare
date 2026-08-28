# Copyright (c) 2026 Martial Systems LLC
"""Locked Nora-window compare. Do not expand to a HUC or a second gage."""

from __future__ import annotations

from pathlib import Path

HUC8 = "05120201"
GAGE_ID = "03351000"
GAGE_NAME = "White River near Nora, IN"
GAGE_NWS_ID = "NORI3"
REFUSED_GAGE_ID = "03353000"
REFUSED_SIR = "2015-5051"
SIR = "2011-5138"
SIR_URL = "https://pubs.usgs.gov/sir/2011/5138/"
GAGE_DATUM_FT_NAVD88 = 710.51
# Partner FIM zeroDatum. Caption the 0.01 ft offset vs Nora's 710.51.
NWS_DATUM_FT_NAVD88 = 710.52
HAND_FLOOD_STAGE_FT = 11.0
HAND_CREST_STAGE_FT = 21.18
HAND_CREST_DATE = "2026-08-15"
HAND_FLOOD_WSE_FT = round(GAGE_DATUM_FT_NAVD88 + HAND_FLOOD_STAGE_FT, 2)
HAND_CREST_WSE_FT = round(GAGE_DATUM_FT_NAVD88 + HAND_CREST_STAGE_FT, 2)
# NWS-served Kim 2011 polygons, named as NAVD88 WSE. Do not interpolate.
PUBLISHED_WSE_FT: tuple[float, ...] = (
    718.0,
    718.5,
    719.5,
    720.5,
    721.5,
    722.5,
    723.5,
    724.5,
    725.5,
    726.5,
    727.5,
    728.5,
    729.5,
    730.5,
    731.5,
    732.5,
)
USGS_FLOOD_WSE_FT = 721.5
USGS_CREST_WSE_FT = 731.5
FT_TO_M = 0.3048
TEMPLATE_CRS = 5070
TEMPLATE_RES_M = 30.0
WET_NODATA = 255
WET_DRY = 0
WET_WET = 1
P_HEADLINE_T = 0.75
P_DEFINITION = "P(sfha | hydro)"
LOCKED_TRANSFORM_SHA256 = (
    "479ac37628bfd7e5d409f6108ae6ba1805acfd37ecdc7093785db06ac9ebec22"
)
LOCKED_BAND_SHA256 = {
    "p_calibrated": "8e1cc7b2178192d6859b3ff6d01014019cf9c5588fbadc3d8b7e228a41ca42c3",
    "zone_class": "1d6c6e39f8f861e71eb4da1b781a12b09a747ab01491e38d641039e75921a0f6",
}
INDIANA_DEFAULT = Path.home() / "indiana_flood_completion"
NORA_DEFAULT = Path.home() / "white_river_stage_inundation"
NORA_LIVE = NORA_DEFAULT / "logs" / "nora_live"
NORA_WET = NORA_LIVE / "rasters" / "wet.tif"
NORA_WET_CREST = NORA_LIVE / "rasters" / "wet_crest_2026-08-15.tif"
NORA_ZONE = NORA_LIVE / "rasters" / "zone_class.tif"
NORA_P = NORA_LIVE / "rasters" / "p_calibrated.tif"
USGS_ZIP_URL = (
    "https://water.noaa.gov/resources/downloads/fim/ind/nori3/shapefile/"
    "nori3_shapefiles.zip"
)
USGS_ZIP_NAME = "nori3_shapefiles.zip"
# Path inside the zip after extract.
USGS_POLY_DIR = Path("shp/ahps/inundation/nori3/polygons")
USER_AGENT = "MartialSystemsResearch/white_river_fim_compare"
ZONE_UNMAPPED = 0
ZONE_SFHA = 1
ZONE_FLOODWAY = 2
ZONE_SHADED_X = 3
ZONE_UNSHADED_X = 4
SFHA_CODES = frozenset({ZONE_SFHA, ZONE_FLOODWAY})
# Fixture template, not the live Nora window.
FIXTURE_WEST = 830_790.0
FIXTURE_NORTH = 1_926_570.0
FIXTURE_ROWS = 16
FIXTURE_COLS = 16
