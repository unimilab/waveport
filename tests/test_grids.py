# ***           **             **************
# ****          ***         ********************
#  ***         ****         ********      ******
#  ***         ****        *****             ****
#  ***         *****       ***                  **
#   ***       ******       **                ** **
#   ***       ******      **             *********
#    **       **  **      **          ************
#    ***     **   ***     *         *************
#     **     **    **    **    *****************
#     ***   ***    ***   **   *****************
#      *******     *******    *************
#      ******       ******    ***
#       *****        ****     ***
#        ***          ***     ***
#
# WavePort — A Python library for reading TICRA Tools files
#
# Licensed under the GNU General Public License 3 or later.
# See the file LICENSE.txt
#
# Copyright © 2026 Maurizio Tomasi

import numpy as np
import pytest

from waveport import (
    ParseError,
    example_data_path,
    ComponentType,
    Grid,
    GridGeometry,
    GridType,
    loads_grid,
)

GRID_DIR = example_data_path()

# File name → (frequencies_hz, grid_type, num_x, num_y, component_type, component_count)
GRID_FILES = {
    "cylindrical.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.PHI_Z,
        13,
        11,
        ComponentType.CO_CROSS,
        3,
    ),
    "planar_rho_phi.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.RHO_PHI,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "planar_xy.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.XY,
        13,
        11,
        ComponentType.CO_CROSS,
        3,
    ),
    "spherical_az_over_el_edx.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.AZIMUTH_OVER_ELEVATION_EDX,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_az_over_el.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.AZIMUTH_OVER_ELEVATION,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_and_az.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_AND_AZIMUTH,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_over_az_edx.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_OVER_AZIMUTH_EDX,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_over_az.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_OVER_AZIMUTH,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_theta_phi.grd":  (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.THETA_PHI,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_uv.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.UV,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "surface.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.UV,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
}

def read_grid_file(name: str) -> str:
    return GRID_DIR.joinpath(name).read_text()


@pytest.mark.parametrize("file_name", sorted(GRID_FILES))
def test_grid_file_parsing(file_name):
    frequencies_hz, grid_type, num_x, num_y, component_type, component_count = GRID_FILES[file_name]

    grids = loads_grid(read_grid_file(file_name))

    assert len(grids) == len(frequencies_hz)
    for idx, grid in enumerate(grids):
        np.testing.assert_allclose(grid.frequency_hz, frequencies_hz[idx])
        assert grid.grid_type == grid_type
        assert grid.num_of_values_along_x == num_x
        assert grid.num_of_values_along_y == num_y
        assert grid.component_type == component_type
        assert grid.component_count == component_count
