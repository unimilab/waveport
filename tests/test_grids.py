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
    frequencies_hz, grid_type, num_x, num_y, component_type, component_count = GRID_FILES[file_name]

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
    np.testing.assert_allclose(first_grid.coefficients[0, 6, :],
                               np.array([0.0 + 1j * 0.1186726861E-01,
                                         -0.2302870825E-20 - 1j * 0.2484383632E-06,
                                         0.8215048165E-03 -1j * 0.5421010862E-19]))
    assert np.all(np.isnan(first_grid.coefficients[0, 7:13, :]))

    # Second row
    assert np.all(np.isnan(first_grid.coefficients[1, 0:3, :]))
    np.testing.assert_allclose(first_grid.coefficients[1, 3:10, :],
                               np.array([[ -0.5293955920E-22 + 1j * 0.8148123646E-06,
                                          0.4523643975E-25 -1j * 0.8154624146E-10,
                                          0.1410158171E-06 + 1j * 0.1323488980E-22],
                                         [0.3388131789E-20 + 1j *  0.5033295072E-04,
                                          -0.2626298445E-22 -1j * 0.3215012277E-08,
                                          0.6968686154E-05 -1j * 0.4235164736E-21],
                                         [-0.2710505431E-19 + 1j * 0.1224346214E-02,
                                          -0.2026592501E-22 - 1j * 0.4389686908E-07,
                                          0.1271342948E-03 + 1j *  0.2541098842E-20],
                                         [0.8673617380E-18 + 1j * 0.1186726953E-01,
                                          -0.3507245797E-20 - 1j * 0.1888172053E-06,
                                          0.8215180298E-03 + 1j *  0.5421010862E-19],
                                         [-0.6938893904E-17 + 1j * 0.4621633767E-01,
                                          -0.2579480022E-19 - 1j * 0.1836682566E-06,
                                          0.1599673218E-02 - 1j * 0.1084202172E-18],
                                         [0.0000000000E+00 + 1j * 0.0000000000E+00,
                                          0.0000000000E+00 + 1j *  0.0000000000E+00,
                                          0.0000000000E+00 + 1j *  0.0000000000E+00],
                                         [-0.6938893904E-17 + 1j * 0.4621633767E-01,
                                          -0.9754113783E-20 - 1j * 0.1836682566E-06,
                                          -0.1599673218E-02 + 1j *  0.1084202172E-18]]))
    assert np.all(np.isnan(first_grid.coefficients[1, 10:13, :]))

    ############################################################
    # Second frequency

    assert second_grid.coefficients.shape == (11, 13, 3)
    
    # First row
    assert np.all(np.isnan(second_grid.coefficients[0, 0:6, :]))
    np.testing.assert_allclose(second_grid.coefficients[0, 6, :],
                               np.array([-0.2710505431E-19 + 1j *  0.1224346001E-02,
                                         -0.2481541838E-23 -1j * 0.5775779960E-07,
                                         0.1271322500E-03 + 1j * 0.5082197684E-20]))
    assert np.all(np.isnan(second_grid.coefficients[0, 7:13, :]))

    # Second row
    assert np.all(np.isnan(second_grid.coefficients[1, 0:3, :]))
    np.testing.assert_allclose(second_grid.coefficients[1, 3:10, :],
                               np.array([
                                   [-0.1893266173E-28 + 1j * 0.4116333717E-12,
                                    0.9860761315E-31 - 1j * 0.9359904611E-16,
                                    0.1068607126E-12 + 1j *  0.6310887242E-29],
                                   [0.2067951531E-24 + 1j * 0.5113878486E-08,
                                    0.1009741959E-27 - 1j * 0.7394941013E-12,
                                    0.1062047543E-08 + 1j *  0.3877409121E-25],
                                   [0.1020674701E-18 + 1j * 0.7201638905E-05,
                                    -0.7677270060E-23 - 1j * 0.5829485208E-09,
                                    0.1121716672E-05 - 1j * 0.1589510265E-19],
                                   [-0.2710505431E-19 + 1j *  0.1224346214E-02,
                                    -0.2026592501E-22 - 1j * 0.4389686908E-07,
                                    0.1271342948E-03 + 1j *  0.2541098842E-20],
                                   [0.0000000000E+00 + 1j * 0.2623651139E-01,
                                    -0.3143286328E-21 - 1j * 0.2346877739E-06,
                                    0.1362176307E-02 + 1j *  0.6776263578E-20],
                                   [0 + 0j,
                                    0 + 0j,
                                    0 + 0j],
                                   [0 + 1j * 0.2623651139E-01,
                                    -0.9140345769E-21 - 1j * 0.2346877739E-06,
                                    -0.1362176307E-02 - 1j * 0.6776263578E-20]]))
    assert np.all(np.isnan(second_grid.coefficients[1, 10:13, :]))
    
