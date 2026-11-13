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

import numpy as np

from waveport._core import (
    Cut,
    CutGeometry,
    CutMode,
    CutType,
    loads_cut,
)

from .common import load_text_file_path


def _angles(self: Cut) -> np.ndarray:
    """Return a NumPy array containing the list of angles that vary in the cut.

    The angle that varies can either be ϑ (polar angle) or φ
    (azimuthal angle). To decide what is the case, refer to
    :attr:`.Cut.mode`.

    Angles are expressed in degrees.

    """

    return self.init_value + np.arange(self.num_of_values_in_cut) * self.increment


Cut.angles = _angles


def load_cut(path: str | Path, geometry: CutGeometry | None = None) -> list[Cut]:
    """Load a cut file given its path

    The function takes the name of the file containing the cut and
    returns a :class:`.Cut` object::

        import waveport

        cut = waveport.load_cut("my_antenna_pattern.cut")

    The function is able to automatically decompress `.gz` and `.bz2`
    files.

    The *geometry* parameter is needed to specify the kind of geometry
    used in the file, as TICRA does not record this information in
    cut files. If you are unsure, leave the default (``None``).

    """
    return load_text_file_path(path, loads_cut, geometry)


############################################################
# Docstrings

CutGeometry.__doc__ = R"""The geometry used in a TICRA cut file

This type is used to record the kind of geometry used in a TICRA cut
file.
"""


CutMode.__doc__ = R"""Which angle in the cut is varying

This type is used to indicate whether the cut was computed along the ϑ
(polar) or φ (azimuthal) angle.

- ``FIXED_AZIMUTH``: the constant angle is φ (azimuth angle), while ϑ
  varies

- ``VARYING_AZIMUTH``: the constant angle is ϑ (polar angle), while φ
  varies
"""


CutType.__doc__ = R"""Type of cut

This type is used to indicate the coordinates used to extract the cut. Refer to the TICRA User’s manual to get the proper definition of each coordinate system.

"""


Cut.__doc__ = """The contents of a TICRA Cut file

This class contains all the information loaded from a ``.cut`` file.

It is typically instantiated by the functions :func:`.loads_cut`
(which reads the contents from a pre-loaded text string) and
:func:`.load_cut` (which takes a filename as parameter and loads its
contents).

"""

Cut.geometry.__doc__ = """The type of geometry used in the cut

The geometry type is expressed through the type :class:`.CutGeometry`.

A word of caution: the TICRA cut file format does not encode the
geometry in the file. This information must be usually provided
externally, i.e., through the parameter *geometry* when calling
:func:`.loads_cut` or :func:`.load_cut`.

"""

Cut.component_count.__doc__ = R"""The number of components per sample.

It can be one of the following values:

- 2: only the tangential components of the electric vector are
  recorded (far field)

- 3: the three components of the electric vector are recorded (near
  field)
"""

Cut.constant_angle.__doc__ = R"""Value of the angle that is kept constant in the cut

The actual angle is determined by the value in :attr:`.Cut.mode`:

- ``FIXED_AZIMUTH``: the constant angle is φ (azimuth angle), while ϑ
  varies

- ``VARYING_AZIMUTH``: the constant angle is ϑ (polar angle), while φ
  varies

The angle is expressed in degrees.
"""

Cut.coefficients.__doc__ = R"""The coefficients of the cut

This is a NumPy array of rank 2 with shape ``(n_points,
n_components)``, where ``n_points`` is the number of points along the
cut and ``n_components`` is either 2 or 3, depending whether it is a
near field or far field simulation.

The value of ``n_points`` is the same as
:attr:`.Cut.num_of_values_in_cut`, while `n_components` is the same as
:attr:`.Cut.component_count`.

"""


Cut.increment.__doc__ = R"""Angle between two consecutive samples

Angle (in degrees) between two consecutive samples in
:attr:`.Cut.coefficients`. This is the increment used in the field
:attr:`.Cut.angles`.

"""


Cut.init_value.__doc__ = R"""First angle in the cut

Angle (in degrees) of the first sample in :attr:`.Cut.coefficients`.
This is the value of the first element in the array
:attr:`.Cut.angles`.

"""


Cut.num_of_values_in_cut.__doc__ = R"""Number of angles sampled by the cut

This is the number of elements in the array :attr:`.Cut.angles`.

"""
