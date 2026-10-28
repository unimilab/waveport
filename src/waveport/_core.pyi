"""Type declarations for the nanobind extension and its Python helpers."""

import enum

import numpy as np
from numpy.typing import NDArray

class ParseError(ValueError): ...

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
