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
import numpy.testing as npt
import pytest

from waveport import (
    example_data_path,
    load_swe,
)

GRID_DIR = example_data_path()
SQRT_2 = np.sqrt(2)


@pytest.mark.parametrize(
    "data_file,reference",
    [
        (
            "hertzian_e_dipole_x.sph.gz",
            {(2, -1, 1): -1j / SQRT_2, (2, 1, 1): 1j / SQRT_2},
        ),
        ("hertzian_e_dipole_y.sph.gz", {(2, -1, 1): 1 / SQRT_2, (2, 1, 1): 1 / SQRT_2}),
        ("hertzian_e_dipole_z.sph.gz", {(2, 0, 1): -1j}),
        (
            "hertzian_h_dipole_x.sph.gz",
            {(1, -1, 1): 1 / SQRT_2, (1, 1, 1): -1 / SQRT_2},
        ),
        (
            "hertzian_h_dipole_y.sph.gz",
            {(1, -1, 1): 1j / SQRT_2, (1, 1, 1): 1j / SQRT_2},
        ),
        ("hertzian_h_dipole_z.sph.gz", {(1, 0, 1): 1}),
    ],
)
def test_hertzian_dipoles(data_file, reference):
    swe_file = load_swe(example_data_path(data_file))

    assert len(swe_file) == 1
    first_swe = swe_file[0]

    npt.assert_allclose(first_swe.cum_power_w, 0.5)

    nmax = first_swe.n_max
    mmax = first_swe.m_max
    for s in (1, 2):
        for n in range(1, nmax + 1):
            for m in range(-mmax, mmax + 1):
                idx = (s, m, n)
                q = first_swe.coefficient(*idx)
                if idx in reference:
                    npt.assert_allclose(q.real, reference[idx].real, atol=1e-12)
                    npt.assert_allclose(q.imag, reference[idx].imag, atol=1e-12)
                else:
                    npt.assert_allclose(q.real, 0.0, atol=1e-12)
                    npt.assert_allclose(q.imag, 0.0, atol=1e-12)


def test_read_multi_frequency():
    swe_file = load_swe(example_data_path("multifrequency_swe.sph.gz"))

    assert len(swe_file) == 3
    assert swe_file[0].frequency_hz == 10.0e9
    npt.assert_allclose(
        swe_file[0].coefficient(1, 0, 1),
        -3.1613714197683554e-17 + 6.7122008842999919e-18j,
    )

    assert swe_file[1].frequency_hz == 15.0e9
    npt.assert_allclose(
        swe_file[1].coefficient(1, 0, 1),
        -3.2613714197683554e-17 + 6.7122008842999919e-18j,
    )

    assert swe_file[2].frequency_hz == 20.0e9
    npt.assert_allclose(
        swe_file[2].coefficient(1, 0, 1),
        -3.3613714197683554e-17 + 6.7122008842999919e-18j,
    )
