"""
config.py
---------
Default settings for map appearance, wind radii colors, and plot layout.
Override any of these by passing keyword arguments into plot functions.
"""

# ---------------------------------------------------------------------------
# Wind radii colors
# ---------------------------------------------------------------------------

#: Color for 34-knot wind radius arcs
COLOR_R34: str = "crimson"

#: Color for 50-knot wind radius arcs
COLOR_R50: str = "blue"

#: Color for 64-knot wind radius arcs
COLOR_R64: str = "green"

#: Line width for wind radii arcs
ARC_LINEWIDTH: float = 2.0

# ---------------------------------------------------------------------------
# Track marker style
# ---------------------------------------------------------------------------

#: Marker size for track points
MARKER_SIZE: float = 7.0

#: Marker edge width
MARKER_EDGE_WIDTH: float = 2.5

#: Marker face color
MARKER_FACE_COLOR: str = "blue"

#: Marker edge color
MARKER_EDGE_COLOR: str = "white"

# ---------------------------------------------------------------------------
# Map layout
# ---------------------------------------------------------------------------

#: Degrees of padding around the storm track bounding box
MAP_OFFSET: float = 10.0

#: Figure size (width, height) in inches
FIGURE_SIZE: tuple[int, int] = (20, 25)

#: Grid line spacing in degrees for longitude
GRID_LON_STEP: int = 10

#: Grid line spacing in degrees for latitude
GRID_LAT_STEP: int = 10

# ---------------------------------------------------------------------------
# Radius scaling
# ---------------------------------------------------------------------------

#: Divisor applied to wind radii (nautical miles) to convert to plot units
#: 70 was the empirically tuned value in the original script
RADIUS_SCALE: float = 70.0

# ---------------------------------------------------------------------------
# Annotation offset (points)
# ---------------------------------------------------------------------------

#: Alternating annotation offsets: (x_positive, y_positive, x_negative, y_negative)
ANNOTATION_OFFSET_POS: tuple[int, int] = (180, 5)
ANNOTATION_OFFSET_NEG: tuple[int, int] = (-280, -5)