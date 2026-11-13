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
    Grid,
    GridGeometry,
    loads_grid,
)

from .common import load_text_file_path


def load_grid(path: str | Path, geometry: GridGeometry | None = None) -> list[Grid]:
    """Load a grid file given its path

    The function takes the name of the file containing the grid and
    returns a :class:`.Grid` object::

        import waveport

        cut = waveport.load_grid("my_antenna_pattern.grid")

    The function is able to automatically decompress `.gz` and `.bz2`
    files.

    The *geometry* parameter is needed to specify the kind of geometry
    used in the file, as TICRA does not record this information in
    grid files. If you are unsure, leave the default (``None``).

    """
    return load_text_file_path(path, loads_grid, geometry)


############################################################
# Docstrings

Grid.__doc__ = """The contents of a TICRA grid file

This class contains all the information loaded from a ``.grd`` file.

It is typically instantiated by the functions :func:`.loads_grid`
(which reads the contents from a pre-loaded text string) and
:func:`.load_grid` (which takes a filename as parameter and loads its
contents).

"""

Grid.geometry.__doc__ = """The type of geometry used in the grid

This is an enumeration :class:`.GridGeometry` that describes the kind
of geometry that was used in the grid.

A word of caution: the TICRA cut file format does not encode the
geometry in the file. This information must be usually provided
externally, i.e., through the parameter *geometry* when calling
:func:`.loads_grid` or :func:`.load_grid`.

"""


Grid.coefficients.__doc__ = R"""The components of the electric field :math:`\vec E`

This is a NumPy array of rank 3 and shape ``(n_y, n_x, n_comp)``,
where ``n_x`` is the fastest-varying angle and ``n_y`` the
slowest-varying angle. The value of ``n_comp`` is either 2 or 3,
whether the simulation was done in the near or far field.

The value of ``n_y`` is the same as
:attr:`.Grid.num_of_values_along_y`, ``n_x`` is the same as
:attr:`.Grid.num_of_values_along_x`, and ``n_comp`` is the same as
:attr:`.Grid.component_count`.

"""


Grid.component_count.__doc__ = R"""The number of components per sample.

It can be one of the following values:

- 2: only the tangential components of the electric vector are
  recorded (far field)

- 3: the three components of the electric vector are recorded (near
  field)
"""


Grid.component_type.__doc__ = R"""The way the polarization vector is encoded.

This type specifies the axes used to decompose the electric vector
:math:`\vec E` along the two transverse directions. Refer to the TICRA
User’s manual for an explanation of each of these entries.

"""


Grid.frequency_hz.__doc__ = R"""The frequency used to compute the coefficients

Frequency (in Hz) used to compute the values of the electric field on
the grid.

"""


Grid.grid_type.__doc__ = R"""Kind of parameterization used for the grid

This is an instance of the :class:`.GridType` enum that specifies how
the grid was defined.

"""


Grid.num_of_values_along_x.__doc__ = R"""Number of values sampled along the X component

The X component is typically an angle, and it is the fastest-varying
one.

"""


Grid.num_of_values_along_y.__doc__ = R"""Number of values sampled along the Y component

The Y component is typically an angle, and it is the slowest-varying
one.

"""


Grid.x_vector.__doc__ = R"""The array of values for the X component

The X component is typically an angle, and it is the fastest-varying
one.

"""


Grid.y_vector.__doc__ = R"""The array of values for the Y component

The Y component is typically an angle, and it is the slowest-varying
one.

"""
