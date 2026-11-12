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

This is an enumeration that describes the kind of geometry
that was used in the grid.

A word of caution: the TICRA cut file format does not encode the
geometry in the file. This information must be usually provided
externally, i.e., through the parameter *geometry* when calling
:func:`.loads_grid` or :func:`.load_grid`.

"""
