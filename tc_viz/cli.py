"""
cli.py
------
Command-line entry point.

Usage
-----
    python -m tc_viz.cli --name IDA --year 2021

Or after ``pip install -e .``:
    tc-viz --name IDA --year 2021
"""

from __future__ import annotations

import argparse

from .config import COLOR_R34, COLOR_R50, COLOR_R64, MAP_OFFSET, RADIUS_SCALE
from .ibtracs import get_storm_track
from .plot import plot_track


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot a TC track with wind radii arcs from IBTrACS data."
    )
    parser.add_argument("--name",  required=True, help="Storm name in uppercase, e.g. IDA")
    parser.add_argument("--year",  required=True, type=int, help="Storm year, e.g. 2021")
    parser.add_argument(
        "--ibt-csv",
        default="ibtracs.ALL.list.v04r00.csv",
        help="Path to IBTrACS CSV file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output PNG path (default: <NAME>_<YEAR>_track.png)",
    )
    parser.add_argument(
        "--map-offset",
        type=float,
        default=MAP_OFFSET,
        help="Degrees of padding around storm track bounding box",
    )
    parser.add_argument("--color-r34", default=COLOR_R34, help="Color for 34-kt wind radii arcs")
    parser.add_argument("--color-r50", default=COLOR_R50, help="Color for 50-kt wind radii arcs")
    parser.add_argument("--color-r64", default=COLOR_R64, help="Color for 64-kt wind radii arcs")
    parser.add_argument(
        "--radius-scale",
        type=float,
        default=RADIUS_SCALE,
        help="Divisor converting nautical miles to plot units (default: 70)",
    )
    parser.add_argument(
        "--no-filter-wmo",
        action="store_true",
        help="Disable WMO wind/pressure filter (use for 2021 data)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    storm_name = args.name.upper()
    output_path = args.output or f"{storm_name}_{args.year}_track.png"

    # 2021 IBTrACS data has blank WMO fields
    filter_wmo = not args.no_filter_wmo and args.year != 2021

    print(f"Loading IBTrACS track for {storm_name} ({args.year})...")
    track = get_storm_track(
        name=storm_name,
        year=args.year,
        ibtracs_csv=args.ibt_csv,
        filter_missing_wmo=filter_wmo,
    )
    print(f"  {len(track)} track points loaded.")

    print("Generating plot...")
    plot_track(
        track=track,
        storm_name=storm_name,
        output_path=output_path,
        map_offset=args.map_offset,
        color_r34=args.color_r34,
        color_r50=args.color_r50,
        color_r64=args.color_r64,
        radius_scale=args.radius_scale,
    )


if __name__ == "__main__":
    main()