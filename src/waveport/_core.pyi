"""Type declarations for the nanobind extension and its Python helpers."""

import enum

import numpy as np
from numpy.typing import NDArray

class ParseError(ValueError): ...

class ComponentType(enum.Enum):
    LINEAR_THETA_PHI = 1
    CIRCULAR = 2
    CO_CROSS = 3
    LINEAR_ALONG_POL_ELLIPSE = 4
    XPD_THETA_PHI = 5
    XPD_CIRCULAR = 6
    XPD_CO_CROSS = 7
    XPD_POL_ELLIPSE = 8
    TOTAL_POWER_AND_CIRCULAR_RATIO = 9
    POYNTING_VECTOR = 11

class CutGeometry(enum.Enum):
    SPHERICAL = 0
    PLANAR = 1
    SURFACE = 2
    CYLINDRICAL = 3

class CutMode(enum.Enum):
    FIXED_AZIMUTH = 1
    VARYING_AZIMUTH = 2

class CutType(enum.Enum):
    POLAR_SPHERICAL = 0
    CONICAL_SPHERICAL = 1
    RADIAL_PLANAR = 2
    CIRCULAR_PLANAR = 3
    RADIAL_SURFACE = 4
    CIRCULAR_SURFACE = 5
    AXIAL_CYLINDRICAL = 6
    CIRCULAR_CYLINDRICAL = 7

class Cut:
    @property
    def geometry(self) -> CutGeometry | None: ...
    @property
    def mode(self) -> CutMode: ...
    @property
    def type(self) -> CutType | None: ...
    @property
    def init_value(self) -> float: ...
    @property
    def increment(self) -> float: ...
    @property
    def constant_angle(self) -> int: ...
    @property
    def num_of_values_in_cut(self) -> int: ...
    @property
    def component_count(self) -> int: ...
    @property
    def coefficients(self) -> NDArray[np.complex128]: ...
    def angles(self) -> NDArray[np.float64]: ...

def loads_cut(contents: str, geometry: CutGeometry | None = None) -> list[Cut]: ...

class GridGeometry(enum.Enum):
    SPHERICAL = 0
    PLANAR = 1
    SURFACE = 2
    CYLINDRICAL = 3

class GridType(enum.Enum):
    UV = 1
    RHO_PHI = 2
    XY = 3
    ELEVATION_OVER_AZIMUTH = 4
    ELEVATION_AND_AZIMUTH = 5
    AZIMUTH_OVER_ELEVATION = 6
    THETA_PHI = 7
    PHI_Z = 8
    AZIMUTH_OVER_ELEVATION_EDX = 9
    ELEVATION_OVER_AZIMUTH_EDX = 10

class Grid:
    @property
    def geometry(self) -> GridGeometry | None: ...
    @property
    def frequency_hz(self) -> float: ...
    @property
    def x_vector(self) -> list[float]: ...
    @property
    def y_vector(self) -> list[float]: ...
    @property
    def grid_type(self) -> GridType: ...
    @property
    def num_of_values_along_x(self) -> int: ...
    @property
    def num_of_values_along_y(self) -> int: ...
    @property
    def component_type(self) -> ComponentType: ...
    @property
    def component_count(self) -> int: ...
    @property
    def coefficients(self) -> NDArray[np.complex128]: ...

def loads_grid(contents: str, geometry: GridGeometry | None = None) -> list[Grid]: ...

class Swe:
    @property
    def frequency_hz(self) -> float | None: ...
    @property
    def num_of_theta(self) -> int: ...
    @property
    def num_of_phi(self) -> int: ...
    @property
    def n_max(self) -> int: ...
    @property
    def m_max(self) -> int: ...
    @property
    def cum_power_w(self) -> float: ...
    def are_indexes_valid(self, s: int, m: int, n: int) -> bool: ...
    def coefficient(self, s: int, m: int, n: int) -> complex: ...

def loads_swe(contents: str) -> list[Swe]: ...
