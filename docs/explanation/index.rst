Field data and geometry
=======================

Cuts sample a field along one varying coordinate, while grids sample a field
along two coordinates. Both store complex field coefficients in NumPy arrays.
Geometry describes the coordinate surface; it is separate from the choice of
field components.

Some TICRA cut codes have more than one interpretation. An explicit
``CutGeometry`` tells the parser whether a cut is spherical, planar, on a
surface, or cylindrical. Without that context, a cut's ``geometry`` and
``type`` may be ``None``. Grid parsing similarly accepts an optional
``GridGeometry``.

The coefficient arrays use sample coordinates as their leading axes and the
field component as their final axis. Grid arrays have shape
``(num_of_values_along_y, num_of_values_along_x, component_count)``.
Missing grid samples can be represented by NumPy ``nan`` values.
