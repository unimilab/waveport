#
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

from pathlib import Path

from waveport._core import (
    Swe,
    loads_swe,
)

from .common import load_text_file_path


def load_swe(path: str | Path) -> list[Swe]:
    """Load a grid file given its path

    The function takes the name of the file containing the SWE
    coefficients and returns a list of :class:`.Swe` objects (one per
    each frequency saved in the file)::

        import waveport

        swe_list = waveport.load_swe("my_antenna_pattern.sph")

    The function is able to automatically decompress `.gz` and `.bz2`
    files.

    """
    return load_text_file_path(path, loads_swe)


############################################################
# Docstrings

Swe.__doc__ = """The contents of a TICRA ``.sph`` file

This class contains all the information loaded from a ``.sph`` file.

It is typically instantiated by the functions :func:`.loads_swe`
(which reads the contents from a pre-loaded text string) and
:func:`.load_swe` (which takes a filename as parameter and loads its
contents).

"""

Swe.frequency_hz.__doc__ = """The radiation frequency

The frequency (in Hz) of the radiation used to compute the coefficients.

WavePort deduces this field from the header, but as it is not formally
documented in the TICRA User’s manual, the extraction of the frequency
might fail. In this case, WavePort sets it to ``None``.

"""

Swe.cum_power_w.__doc__ = R"""Return the cumulative power of the SWE coefficients

This variable contains the sum of the power encoded by all the
:math:`Q_{smn}` coefficients read from the file. Its value is
expressed in Watt.

"""

Swe.num_of_theta.__doc__ = """Number of ϑ-samples over 360°

This number must be even and ≥4.

"""

Swe.num_of_phi.__doc__ = """Number of φ-samples over 360°

This number must be ≥3.

"""

Swe.n_max.__doc__ = """Maximum value for the polar index :math:`n`

The number must be between 1 and :attr:`.Swe.num_of_theta`/2

"""

Swe.m_max.__doc__ = r"""Maximum value for the azimuthal index :math:`\left|m\right|`

The number must be between 1 and :attr:`.Swe.num_of_theta`/2

"""

Swe.num_of_coefficients.__doc__ = """Number of coefficients stored in memory

This represents the *actual* number of complex coefficients
:math:`Q_{smn}` stored in memory by the :class:`.Swe` object.

"""
