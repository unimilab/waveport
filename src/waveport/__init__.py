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

import numpy as np

from waveport._core import (
    ParseError,
    ComponentType,
    Cut,
    CutGeometry,
    CutMode,
    CutType,
    loads_cut,
    Grid,
    GridGeometry,
    GridType,
    loads_grid,
)

from .example_files import (
    example_data_path,
)

################################################################################
# Cut


def _angles(self: Cut) -> np.ndarray:
    """Return a NumPy array containing the list of angles that vary in the cut"""

    return self.init_value + np.arange(self.num_of_values_in_cut) * self.increment


Cut.angles = _angles

################################################################################

__all__ = [
    # waveport._core
    "ParseError",
    "ComponentType",
    "Cut",
    "CutGeometry",
    "CutMode",
    "CutType",
    "loads_cut",
    "Grid",
    "GridGeometry",
    "GridType",
    "loads_grid",
    # example_files.py
    "example_data_path",
]
