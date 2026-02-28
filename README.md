# tc-viz

**tc-viz** is a data visualization tool for exploring tropical cyclone lifecycles using data from the [International Best Track Archive for Climate Stewardship (IBTrACS)](https://www.ncei.noaa.gov/products/international-best-track-archive). Given a storm name and year, the package generates detailed maps illustrating the storm's path alongside wind radii in four quadrants, wind intensity, and pressure variations over time. Built during an R&D internship at NOAA, this tool is currently used by NOAA scientists for gaining insights on the severity of tropical cyclones and for reporting purposes.

## Installation

```bash
git clone https://github.com/your-username/tc-viz.git
cd tc-viz
pip install -e .
```

## Usage

**Command line**
```bash
# Basic usage
tc-viz --name IDA --year 2021

# Custom output path and colors
tc-viz --name IDA --year 2021 --output ida_track.png --color-r34 red --color-r50 blue --color-r64 green

# Disable WMO filter for 2021 data
tc-viz --name IDA --year 2021 --no-filter-wmo
```

**Python API**
```python
from tc_viz import get_storm_track, plot_track

track = get_storm_track("IDA", 2021, "ibtracs.ALL.list.v04r00.csv", filter_missing_wmo=False)

plot_track(track, storm_name="IDA", output_path="IDA_2021_track.png")
```

## Required data files

| File | Source |
|---|---|
| `ibtracs.ALL.list.v04r00.csv` | [IBTrACS downloads](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/) |

## Map features

Visualizations are rendered using Cartopy's PlateCarree projection with coastlines and national borders. The map auto-zooms to the storm track bounding box with configurable padding. Each track point is annotated with date/time, wind speed (kt), and pressure (hPa), with alternating label offsets to reduce overlap.

**Wind radii** are drawn per quadrant (NE, NW, SE, SW) for three wind thresholds:
- 34-knot radius — crimson (default)
- 50-knot radius — blue (default)
- 64-knot radius — green (default)

Output is saved as a PNG file, serving as a valuable resource for researchers, meteorologists, and anyone interested in tropical cyclone dynamics.

## Package structure

```
tc_viz/
├── __init__.py    — public API
├── config.py      — colors, marker styles, map layout defaults
├── ibtracs.py     — IBTrACS CSV loading and filtering
├── plot.py        — map setup and wind radii drawing functions
└── cli.py         — command-line entry point
```

## Key functions

| Function | Description |
|---|---|
| `get_storm_track(name, year, ibtracs_csv)` | Loads and filters IBTrACS track data for a named storm |
| `plot_track(track, storm_name, output_path)` | Generates the full track map with wind radii and annotations |
| `draw_wind_radii_arcs(xcenter, ycenter, radii, ax)` | Draws quadrant wind radii arcs around a storm center point |

## Notes

- IBTrACS 2021 data has incomplete WMO fields; use `--no-filter-wmo` or `filter_missing_wmo=False` for that year
- Wind radii values (nautical miles) are scaled by a divisor (default: 70) to convert to plot units — adjust `--radius-scale` if arcs appear too large or too small
- All colors, marker styles, and layout defaults can be overridden via `config.py` or function arguments
- The IBTrACS CSV file must follow the standard `ibtracs.ALL.list.v04r00.csv` format



