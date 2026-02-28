"""
plot.py
-------
Functions for drawing TC track maps with wind radii arcs.
"""

from __future__ import annotations

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import pandas as pd

from .config import (
    ARC_LINEWIDTH,
    ANNOTATION_OFFSET_NEG,
    ANNOTATION_OFFSET_POS,
    COLOR_R34,
    COLOR_R50,
    COLOR_R64,
    FIGURE_SIZE,
    GRID_LAT_STEP,
    GRID_LON_STEP,
    MAP_OFFSET,
    MARKER_EDGE_COLOR,
    MARKER_EDGE_WIDTH,
    MARKER_FACE_COLOR,
    MARKER_SIZE,
    RADIUS_SCALE,
)


# ---------------------------------------------------------------------------
# Wind radii drawing helpers
# ---------------------------------------------------------------------------

def draw_wind_radii_arcs(
    xcenter: float,
    ycenter: float,
    radii: list[float],
    ax,
    lw: float = ARC_LINEWIDTH,
    ec: str = COLOR_R34,
) -> None:
    """
    Draw four quadrant arcs representing a wind radius ring.

    Quadrant order: SE, NE, SW, NW (matching IBTrACS column order).

    Parameters
    ----------
    xcenter, ycenter:
        Centre point of the arcs in projected coordinates.
    radii:
        List of four radii ``[SE, NE, SW, NW]`` in plot units.
    ax:
        Matplotlib axes to draw on.
    lw:
        Line width.
    ec:
        Edge/line color.
    """
    for rad, theta in zip(radii, [0, 90, 180, 270]):
        arc = patches.Arc(
            (xcenter, ycenter), 2 * rad, 2 * rad,
            theta1=theta, theta2=theta + 90,
            lw=lw, ec=ec, fc="none",
        )
        ax.add_patch(arc)

    # Horizontal spokes
    ax.hlines(
        [ycenter, ycenter],
        [xcenter + radii[0], xcenter - radii[1]],
        [xcenter + radii[3], xcenter - radii[2]],
        lw=lw, colors=ec,
    )
    # Vertical spokes
    ax.vlines(
        [xcenter, xcenter],
        [ycenter + radii[0], ycenter - radii[2]],
        [ycenter + radii[1], ycenter - radii[3]],
        lw=lw, colors=ec,
    )


def _parse_radii(row: pd.Series, prefix: str, scale: float = RADIUS_SCALE) -> list[float] | None:
    """
    Extract and scale the four quadrant radii for a given wind threshold.

    Returns ``None`` if any quadrant value is missing.

    Parameters
    ----------
    row:
        A single row from the IBTrACS track DataFrame.
    prefix:
        Column prefix, e.g. ``"USA_R34"`` or ``"USA_R50"``.
    scale:
        Divisor to convert nautical miles to plot units.
    """
    quads = [f"{prefix}_{q}" for q in ["SE", "NE", "SW", "NW"]]
    values = [row[q] for q in quads]
    if any(v == " " or pd.isna(v) for v in values):
        return None
    return [int(v) / scale for v in values]


# ---------------------------------------------------------------------------
# Map setup
# ---------------------------------------------------------------------------

def _setup_map(
    ax,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    offset: float = MAP_OFFSET,
) -> None:
    """Configure the cartopy axes with coastlines, borders, and gridlines."""
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent(
        [min_lon - offset, max_lon + offset, min_lat - offset, max_lat + offset],
        crs=ccrs.PlateCarree(),
    )

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(), linewidth=2, color="black",
        alpha=0.5, linestyle="--", draw_labels=True,
    )
    gl.xlabels_top = False
    gl.ylabels_left = False
    gl.ylabels_right = True
    gl.xlines = True

    gl.xlocator = mticker.FixedLocator(range(-180, 190, GRID_LON_STEP))
    gl.ylocator = mticker.FixedLocator(range(-80, 90, GRID_LAT_STEP))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {"weight": "bold"}


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def plot_track(
    track: pd.DataFrame,
    storm_name: str,
    output_path: str | None = None,
    figsize: tuple[int, int] = FIGURE_SIZE,
    map_offset: float = MAP_OFFSET,
    color_r34: str = COLOR_R34,
    color_r50: str = COLOR_R50,
    color_r64: str = COLOR_R64,
    radius_scale: float = RADIUS_SCALE,
) -> plt.Figure:
    """
    Plot a TC track with wind radii arcs and time/wind/pressure annotations.

    Parameters
    ----------
    track:
        DataFrame returned by :func:`ibtracs.get_storm_track`.
    storm_name:
        Used in the output filename if ``output_path`` is auto-generated.
    output_path:
        Path to save the PNG. If ``None``, the figure is shown interactively.
    figsize:
        Figure size ``(width, height)`` in inches.
    map_offset:
        Degrees of padding around the storm track bounding box.
    color_r34, color_r50, color_r64:
        Colors for 34-, 50-, and 64-knot wind radius arcs.
    radius_scale:
        Divisor converting nautical miles to plot units.

    Returns
    -------
    plt.Figure
        The completed matplotlib Figure object.
    """
    crs_latlon = ccrs.PlateCarree()

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1, projection=crs_latlon)

    # Map bounds from track extent
    lats = track["LAT"].astype(float)
    lons = track["LON"].astype(float)
    _setup_map(ax, lats.min(), lats.max(), lons.min(), lons.max(), offset=map_offset)

    sign = 1

    for i in range(len(track)):
        row = track.iloc[i]
        lon = float(row["LON"])
        lat = float(row["LAT"])
        at_x, at_y = ax.projection.transform_point(lon, lat, src_crs=crs_latlon)

        # Draw wind radii arcs for each threshold
        for prefix, color in [
            ("USA_R34", color_r34),
            ("USA_R50", color_r50),
            ("USA_R64", color_r64),
        ]:
            radii = _parse_radii(row, prefix, scale=radius_scale)
            if radii is not None:
                draw_wind_radii_arcs(at_x, at_y, radii, ax=ax, ec=color)

        # Track marker
        ax.plot(
            lon, lat,
            marker="o",
            markersize=MARKER_SIZE,
            markeredgewidth=MARKER_EDGE_WIDTH,
            markerfacecolor=MARKER_FACE_COLOR,
            markeredgecolor=MARKER_EDGE_COLOR,
            transform=crs_latlon,
        )

        # Annotation: date/time, wind, pressure
        time_str = row["ISO_TIME"].strftime("%d/%H") + "Z"
        info_str = f"{time_str}, {row['WMO_WIND']} KTS, {row['WMO_PRES']} hPa"

        x_off, y_off = ANNOTATION_OFFSET_POS if sign > 0 else ANNOTATION_OFFSET_NEG
        ax.annotate(
            info_str,
            xy=(at_x, at_y),
            xytext=(x_off, y_off),
            textcoords="offset points",
            color="black",
            backgroundcolor="white",
            size="large",
            arrowprops=dict(arrowstyle="-", color="black", linewidth=1.0),
        )
        sign *= -1

    if output_path:
        plt.savefig(output_path, bbox_inches="tight")
        print(f"Plot saved to: {output_path}")
    else:
        plt.show()

    return fig