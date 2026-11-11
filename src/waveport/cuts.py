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
    loads_cut,
)

from .common import load_text_file_path


def _angles(self: Cut) -> np.ndarray:
    """Return a NumPy array containing the list of angles that vary in the cut"""

    return self.init_value + np.arange(self.num_of_values_in_cut) * self.increment


Cut.angles = _angles


def load_cut(path: str | Path) -> list[Cut]:
    return load_text_file_path(path, loads_cut)
