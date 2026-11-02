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
    ComponentType,
    GridType,
    example_data_path,
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
        3,
    ),
    "planar_xy.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.XY,
        13,
        11,
        ComponentType.CO_CROSS,
        3,
    ),
    "spherical_az_over_el_edx.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.AZIMUTH_OVER_ELEVATION_EDX,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_az_over_el.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.AZIMUTH_OVER_ELEVATION,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_and_az.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_AND_AZIMUTH,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_over_az_edx.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_OVER_AZIMUTH_EDX,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_el_over_az.grd": (
        [10.0e9, 15.0e9, 20.0e9],
        GridType.ELEVATION_OVER_AZIMUTH,
        13,
        11,
        ComponentType.CO_CROSS,
        2,
    ),
    "spherical_theta_phi.grd": (
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
        None,
        GridType.XY,
        13,
        11,
        ComponentType.CO_CROSS,
        3,
    ),
}


def read_grid_file(name: str) -> str:
    return GRID_DIR.joinpath(name).read_text()


@pytest.mark.parametrize("file_name", sorted(GRID_FILES))
def test_grid_file_parsing(file_name):
    frequencies_hz, grid_type, num_x, num_y, component_type, component_count = (
        GRID_FILES[file_name]
    )

    grids = loads_grid(read_grid_file(file_name))

    if frequencies_hz:
        assert len(grids) == len(frequencies_hz)

    for idx, grid in enumerate(grids):
        if frequencies_hz:
            np.testing.assert_allclose(grid.frequency_hz, frequencies_hz[idx])

        assert grid.grid_type == grid_type
        assert grid.num_of_values_along_x == num_x
        assert grid.num_of_values_along_y == num_y
        assert grid.component_type == component_type
        assert grid.component_count == component_count


def test_implicit_grid():
    grids = loads_grid(read_grid_file("planar_rho_phi.grd"))

    # We could check every line in the three grids, but then the code would be too long
    # and boring. We just check the first two lines of the first two
    # frequencies. All the debugging I did on the C++ code used just
    # these cases and gave me enough confidence that my implementation
    # was correct, so let’s keep fingers crossed and hope that this
    # holds here too…

    first_grid, second_grid, _ = grids

    ############################################################
    # First frequency

    assert first_grid.coefficients.shape == (11, 13, 3)

    # First row
    assert np.all(np.isnan(first_grid.coefficients[0, 0:6, :]))
    np.testing.assert_allclose(
        first_grid.coefficients[0, 6, :],
        np.array(
            [
                0.0 + 1j * 0.1186726861e-01,
                -0.2302870825e-20 - 1j * 0.2484383632e-06,
                0.8215048165e-03 - 1j * 0.5421010862e-19,
            ]
        ),
    )
    assert np.all(np.isnan(first_grid.coefficients[0, 7:13, :]))

    # Second row
    assert np.all(np.isnan(first_grid.coefficients[1, 0:3, :]))
    np.testing.assert_allclose(
        first_grid.coefficients[1, 3:10, :],
        np.array(
            [
                [
                    -0.5293955920e-22 + 1j * 0.8148123646e-06,
                    0.4523643975e-25 - 1j * 0.8154624146e-10,
                    0.1410158171e-06 + 1j * 0.1323488980e-22,
                ],
                [
                    0.3388131789e-20 + 1j * 0.5033295072e-04,
                    -0.2626298445e-22 - 1j * 0.3215012277e-08,
                    0.6968686154e-05 - 1j * 0.4235164736e-21,
                ],
                [
                    -0.2710505431e-19 + 1j * 0.1224346214e-02,
                    -0.2026592501e-22 - 1j * 0.4389686908e-07,
                    0.1271342948e-03 + 1j * 0.2541098842e-20,
                ],
                [
                    0.8673617380e-18 + 1j * 0.1186726953e-01,
                    -0.3507245797e-20 - 1j * 0.1888172053e-06,
                    0.8215180298e-03 + 1j * 0.5421010862e-19,
                ],
                [
                    -0.6938893904e-17 + 1j * 0.4621633767e-01,
                    -0.2579480022e-19 - 1j * 0.1836682566e-06,
                    0.1599673218e-02 - 1j * 0.1084202172e-18,
                ],
                [
                    0.0000000000e00 + 1j * 0.0000000000e00,
                    0.0000000000e00 + 1j * 0.0000000000e00,
                    0.0000000000e00 + 1j * 0.0000000000e00,
                ],
                [
                    -0.6938893904e-17 + 1j * 0.4621633767e-01,
                    -0.9754113783e-20 - 1j * 0.1836682566e-06,
                    -0.1599673218e-02 + 1j * 0.1084202172e-18,
                ],
            ]
        ),
    )
    assert np.all(np.isnan(first_grid.coefficients[1, 10:13, :]))

    ############################################################
    # Second frequency

    assert second_grid.coefficients.shape == (11, 13, 3)

    # First row
    assert np.all(np.isnan(second_grid.coefficients[0, 0:6, :]))
    np.testing.assert_allclose(
        second_grid.coefficients[0, 6, :],
        np.array(
            [
                -0.2710505431e-19 + 1j * 0.1224346001e-02,
                -0.2481541838e-23 - 1j * 0.5775779960e-07,
                0.1271322500e-03 + 1j * 0.5082197684e-20,
            ]
        ),
    )
    assert np.all(np.isnan(second_grid.coefficients[0, 7:13, :]))

    # Second row
    assert np.all(np.isnan(second_grid.coefficients[1, 0:3, :]))
    np.testing.assert_allclose(
        second_grid.coefficients[1, 3:10, :],
        np.array(
            [
                [
                    -0.1893266173e-28 + 1j * 0.4116333717e-12,
                    0.9860761315e-31 - 1j * 0.9359904611e-16,
                    0.1068607126e-12 + 1j * 0.6310887242e-29,
                ],
                [
                    0.2067951531e-24 + 1j * 0.5113878486e-08,
                    0.1009741959e-27 - 1j * 0.7394941013e-12,
                    0.1062047543e-08 + 1j * 0.3877409121e-25,
                ],
                [
                    0.1020674701e-18 + 1j * 0.7201638905e-05,
                    -0.7677270060e-23 - 1j * 0.5829485208e-09,
                    0.1121716672e-05 - 1j * 0.1589510265e-19,
                ],
                [
                    -0.2710505431e-19 + 1j * 0.1224346214e-02,
                    -0.2026592501e-22 - 1j * 0.4389686908e-07,
                    0.1271342948e-03 + 1j * 0.2541098842e-20,
                ],
                [
                    0.0000000000e00 + 1j * 0.2623651139e-01,
                    -0.3143286328e-21 - 1j * 0.2346877739e-06,
                    0.1362176307e-02 + 1j * 0.6776263578e-20,
                ],
                [0 + 0j, 0 + 0j, 0 + 0j],
                [
                    0 + 1j * 0.2623651139e-01,
                    -0.9140345769e-21 - 1j * 0.2346877739e-06,
                    -0.1362176307e-02 - 1j * 0.6776263578e-20,
                ],
            ]
        ),
    )
    assert np.all(np.isnan(second_grid.coefficients[1, 10:13, :]))
