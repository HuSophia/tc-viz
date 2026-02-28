"""
ibtracs.py
----------
Functions for reading and filtering IBTrACS storm track data.
Mirrors the equivalent module in tcmirs but kept standalone so
tc_viz has no cross-repo dependency.
"""

from __future__ import annotations

import pandas as pd


# ---------------------------------------------------------------------------
# Variables extracted from IBTrACS CSV
# ---------------------------------------------------------------------------

_EXTRACT_VARS: list[str] = [
    "NAME", "ISO_TIME", "WMO_WIND", "WMO_PRES", "LAT", "LON",
    "USA_R34_NE", "USA_R34_NW", "USA_R34_SE", "USA_R34_SW",
    "USA_R50_NE", "USA_R50_NW", "USA_R50_SE", "USA_R50_SW",
    "USA_R64_NE", "USA_R64_NW", "USA_R64_SE", "USA_R64_SW",
    "REUNION_R34_NE", "REUNION_R34_NW", "REUNION_R34_SE", "REUNION_R34_SW",
    "REUNION_R50_NE", "REUNION_R50_NW", "REUNION_R50_SE", "REUNION_R50_SW",
    "REUNION_R64_NE", "REUNION_R64_NW", "REUNION_R64_SE", "REUNION_R64_SW",
    "BOM_R34_NE", "BOM_R34_SE", "BOM_R34_NW", "BOM_R34_SW",
    "BOM_R50_NE", "BOM_R50_SE", "BOM_R50_NW", "BOM_R50_SW",
    "BOM_R64_NE", "BOM_R64_SE", "BOM_R64_NW", "BOM_R64_SW",
]


def _lon_to_360(dlon: float) -> float:
    """Convert longitude from -180/180 to 0-360 degrees."""
    return (360 + (dlon % 360)) % 360


def get_storm_track(
    name: str,
    year: int,
    ibtracs_csv: str,
    filter_missing_wmo: bool = True,
) -> pd.DataFrame:
    """
    Load IBTrACS CSV data and return track rows for a named storm in a given year.

    Parameters
    ----------
    name:
        Storm name in uppercase, e.g. ``"IDA"``.
    year:
        Four-digit calendar year of the storm, e.g. ``2021``.
    ibtracs_csv:
        Path to the IBTrACS ``*.list.v04r00.csv`` file.
    filter_missing_wmo:
        If ``True`` (default), rows with missing WMO wind or pressure are
        dropped. Set to ``False`` for years like 2021 where WMO fields may
        be blank in early data.

    Returns
    -------
    pd.DataFrame
        Filtered track data with ``LON_180`` (original longitude) and
        ``LON`` converted to 0-360 degrees.
    """
    data = pd.read_csv(ibtracs_csv, low_memory=False)
    data = data.iloc[1:, :]  # drop units row

    year_start = pd.to_datetime(str(year))
    year_end = pd.to_datetime(str(year + 1))

    data = data[data["NAME"] == name]
    data["ISO_TIME"] = pd.to_datetime(data["ISO_TIME"])

    mask = (data["ISO_TIME"] >= year_start) & (data["ISO_TIME"] < year_end)
    data = data[mask]
    data = data[_EXTRACT_VARS]

    if filter_missing_wmo:
        data = data[data["WMO_WIND"] != " "]
        data = data[data["WMO_PRES"] != " "]

    data["LON_180"] = data["LON"]
    data["LON"] = data["LON"].astype(float).apply(_lon_to_360)

    return data