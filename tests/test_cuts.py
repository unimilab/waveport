# -*- encoding: utf-8 -*-
#
# ***                              ***********
# ****                            ***************
#  ***                           ****          ***
#   ***                          ****       ******
#    ***                        **               **
#    ****        ******        ***            ****
#     ****      *********     ***  ***************
#      ****    ***********    ***  *************
#       *********      *********   ****
#       ********        ********   ***
#         ***             ****     ***
#
# WavePort — A Python library for reading TICRA Tools files
#
# Licensed under the GNU General Public License 3 or later.
# See the file LICENSE.txt
#
# Copyright © 2026 Maurizio Tomasi

import pytest

import numpy as np

from waveport import example_data_path, read_cut
from waveport._core import CutGeometry, CutMode, CutType, ParseError, loads_cut

CUT_DIR = example_data_path("TICRA-models", "simple", "working")

# File name → (geometry, expected ICUT mode, expected cut type, number of cuts)
CUT_FILES = {
    "polar_spherical.cut": (
        CutGeometry.SPHERICAL,
        CutMode.FIXED_AZIMUTH,
        CutType.POLAR_SPHERICAL,
        8,
    ),
    "conical_spherical.cut": (
        CutGeometry.SPHERICAL,
        CutMode.VARYING_AZIMUTH,
        CutType.CONICAL_SPHERICAL,
        6,
    ),
    "radial_planar.cut": (
        CutGeometry.PLANAR,
        CutMode.FIXED_AZIMUTH,
        CutType.RADIAL_PLANAR,
        8,
    ),
    "circular_planar.cut": (
        CutGeometry.PLANAR,
        CutMode.VARYING_AZIMUTH,
        CutType.CIRCULAR_PLANAR,
        6,
    ),
    "radial_surface.cut": (
        CutGeometry.SURFACE,
        CutMode.FIXED_AZIMUTH,
        CutType.RADIAL_SURFACE,
        8,
    ),
    "circular_surface.cut": (
        CutGeometry.SURFACE,
        CutMode.VARYING_AZIMUTH,
        CutType.CIRCULAR_SURFACE,
        6,
    ),
    "axial_cylindrical.cut": (
        CutGeometry.CYLINDRICAL,
        CutMode.FIXED_AZIMUTH,
        CutType.AXIAL_CYLINDRICAL,
        8,
    ),
    "circular_cylindrical.cut": (
        CutGeometry.CYLINDRICAL,
        CutMode.VARYING_AZIMUTH,
        CutType.CIRCULAR_CYLINDRICAL,
        6,
    ),
}


def read_cut_file(name: str) -> str:
    return CUT_DIR.joinpath(name).read_text()


def replace_icut(contents: str, new_icut: str) -> str:
    """Replace the ICUT field in the header of the first cut"""
    lines = contents.splitlines(keepends=True)
    fields = lines[1].split()
    fields[5] = new_icut
    lines[1] = " ".join(fields) + "\n"
    return "".join(lines)


def test_basic_load():
    cuts = read_cut()
    print(cuts)


@pytest.mark.parametrize("file_name", sorted(CUT_FILES))
def test_icut_parsing(file_name):
    geometry, mode, cut_type, num_of_cuts = CUT_FILES[file_name]

    cuts = loads_cut(read_cut_file(file_name), geometry)

    assert len(cuts) == num_of_cuts
    for cut in cuts:
        assert cut.geometry == geometry
        assert cut.mode == mode
        assert cut.type == cut_type


def test_coefficients():
    cuts = loads_cut(read_cut_file("radial_planar.cut"), CutGeometry.PLANAR)

    assert len(cuts) == 8

    # Cut #1
    np.testing.assert_allclose(
        cuts[0].coefficients,
        np.array(
            [
                [
                    0.4128450220e00 + 0.9298980786e-01j,
                    -0.1818652480e-16 + 0.4522820866e-15j,
                    -0.7393007485e-16 + 0.6532329100e-16j,
                ],
                [
                    -0.3843530718e-04 + 0.1454952464e-04j,
                    0.9951549043e-17 - 0.2498880306e-16j,
                    0.1578750538e-03 + 0.4377333644e-03j,
                ],
                [
                    -0.7290271392e-05 - 0.6342868257e-06j,
                    0.7670689622e-18 - 0.1175613604e-17j,
                    0.2656977095e-04 + 0.4396189541e-03j,
                ],
            ]
        ),
    )

    # Cut #2
    np.testing.assert_allclose(
        cuts[1].coefficients,
        np.array(
            [
                [
                    0.4128450220e00 + 0.9298980786e-01j,
                    -0.1818652480e-16 + 0.4522820866e-15j,
                    -0.7393007485e-16 + 0.6532329100e-16j,
                ],
                [
                    -0.2411610455e-02 - 0.1126860008e-03j,
                    -0.1570244249e-02 - 0.2468369464e-03j,
                    -0.1299954329e-02 - 0.8416240945e-03j,
                ],
                [
                    -0.4145816380e-02 + 0.6015268033e-03j,
                    -0.2357261834e-02 + 0.3168243852e-03j,
                    -0.2795197653e-04 - 0.3555235878e-03j,
                ],
            ]
        ),
    )

    # Cut #3
    np.testing.assert_allclose(
        cuts[2].coefficients,
        np.array(
            [
                [
                    0.4128450220e00 + 0.9298980786e-01j,
                    -0.1818652480e-16 + 0.4522820866e-15j,
                    -0.7393007485e-16 + 0.6532329100e-16j,
                ],
                [
                    -0.2411610455e-02 - 0.1126860008e-03j,
                    0.1570244249e-02 + 0.2468369464e-03j,
                    -0.1299954329e-02 - 0.8416240945e-03j,
                ],
                [
                    -0.4145816380e-02 + 0.6015268033e-03j,
                    0.2357261834e-02 - 0.3168243852e-03j,
                    -0.2795197653e-04 - 0.3555235878e-03j,
                ],
            ]
        ),
    )

    # Cut #4
    np.testing.assert_allclose(
        cuts[3].coefficients,
        np.array(
            [
                [
                    0.4128450220e00 + 0.9298980786e-01j,
                    -0.1818652480e-16 + 0.4522820866e-15j,
                    -0.7393007485e-16 + 0.6532329100e-16j,
                ],
                [
                    -0.3843530718e-04 + 0.1454952464e-04j,
                    0.9476976819e-17 - 0.1734994880e-16j,
                    0.1578750538e-03 + 0.4377333644e-03j,
                ],
                [
                    -0.7290271392e-05 - 0.6342868257e-06j,
                    0.3823782599e-17 + 0.7959537337e-18j,
                    0.2656977095e-04 + 0.4396189541e-03j,
                ],
            ]
        ),
    )

    # Cut #5
    np.testing.assert_allclose(
        cuts[4].coefficients,
        np.array(
            [
                [
                    -0.1967114520e-01 - 0.1334150629e00j,
                    0.2535874999e-15 - 0.3312068383e-15j,
                    -0.3074254202e-16 - 0.1306046129e-15j,
                ],
                [
                    0.2697099053e-04 - 0.2635506307e-04j,
                    0.2067512963e-16 + 0.1211389891e-16j,
                    0.4554163451e-03 - 0.1766796430e-03j,
                ],
                [
                    0.5574259068e-05 - 0.3271439341e-05j,
                    -0.1117262680e-17 + 0.1944544138e-17j,
                    0.7459792324e-03 - 0.2859316202e-03j,
                ],
            ]
        ),
    )

    # Cut #6
    np.testing.assert_allclose(
        cuts[5].coefficients,
        np.array(
            [
                [
                    -0.1967114520e-01 - 0.1334150629e00j,
                    0.2535874999e-15 - 0.3312068383e-15j,
                    -0.3074254202e-16 - 0.1306046129e-15j,
                ],
                [
                    -0.1981295128e-02 + 0.4533611146e-03j,
                    -0.9911907908e-03 + 0.3333596232e-03j,
                    -0.9327637025e-04 - 0.7508972265e-04j,
                ],
                [
                    0.8021188026e-03 + 0.2059903629e-02j,
                    0.5637960181e-03 + 0.1279170508e-02j,
                    0.3168459976e-03 + 0.6326347455e-03j,
                ],
            ]
        ),
    )

    # Cut #7
    np.testing.assert_allclose(
        cuts[6].coefficients,
        np.array(
            [
                [
                    -0.1967114520e-01 - 0.1334150629e00j,
                    0.2535874999e-15 - 0.3312068383e-15j,
                    -0.3074254202e-16 - 0.1306046129e-15j,
                ],
                [
                    -0.1981295128e-02 + 0.4533611146e-03j,
                    0.9911907908e-03 - 0.3333596232e-03j,
                    -0.9327637025e-04 - 0.7508972265e-04j,
                ],
                [
                    0.8021188026e-03 + 0.2059903629e-02j,
                    -0.5637960181e-03 - 0.1279170508e-02j,
                    0.3168459976e-03 + 0.6326347455e-03j,
                ],
            ]
        ),
    )

    # Cut #8
    np.testing.assert_allclose(
        cuts[7].coefficients,
        np.array(
            [
                [
                    -0.1967114520e-01 - 0.1334150629e00j,
                    0.2535874999e-15 - 0.3312068383e-15j,
                    -0.3074254202e-16 - 0.1306046129e-15j,
                ],
                [
                    0.2697099053e-04 - 0.2635506307e-04j,
                    0.4194733736e-17 + 0.1038896062e-16j,
                    0.4554163451e-03 - 0.1766796430e-03j,
                ],
                [
                    0.5574259068e-05 - 0.3271439341e-05j,
                    -0.6730307156e-17 + 0.1448242438e-16j,
                    0.7459792324e-03 - 0.2859316202e-03j,
                ],
            ]
        ),
    )


def test_icut_parsing_without_geometry():
    cuts = loads_cut(read_cut_file("polar_spherical.cut"))

    for cut in cuts:
        assert cut.geometry is None
        assert cut.mode == CutMode.FIXED_AZIMUTH
        assert cut.type is None


def test_repr():
    cuts = loads_cut(read_cut_file("circular_planar.cut"), CutGeometry.PLANAR)

    assert (
        repr(cuts[0])
        == "Cut(geometry=CutGeometry.PLANAR, mode=CutMode.VARYING_AZIMUTH)"
    )


def test_parse_error_is_value_error():
    assert issubclass(ParseError, ValueError)


@pytest.mark.parametrize("icut", ["0", "3", "-1"])
def test_invalid_icut(icut):
    contents = replace_icut(read_cut_file("polar_spherical.cut"), icut)

    with pytest.raises(ParseError, match=f"Invalid value {icut} for ICUT"):
        loads_cut(contents)


def test_non_numeric_icut():
    contents = replace_icut(read_cut_file("polar_spherical.cut"), "X")

    with pytest.raises(ParseError, match="invalid number"):
        loads_cut(contents)


def test_missing_header():
    with pytest.raises(ParseError, match="reading the cut header"):
        loads_cut("Field data in cuts\n")


def test_header_with_missing_fields():
    with pytest.raises(ParseError, match="missing value"):
        loads_cut("Field data in cuts\n  0.0 1.0 3 0.0 3 1\n")


def test_header_with_extra_fields():
    with pytest.raises(ParseError, match="unexpected extra content"):
        loads_cut("Field data in cuts\n  0.0 1.0 3 0.0 3 1 3 4\n")


def test_truncated_field_data():
    lines = read_cut_file("polar_spherical.cut").splitlines(keepends=True)

    # Keep the title, the header, and only one of the three field lines
    with pytest.raises(ParseError, match="Unexpected empty content"):
        loads_cut("".join(lines[:3]))
