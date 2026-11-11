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

from importlib.resources import files
from pathlib import Path


def example_data_path(*parts: str) -> Path:
    """Return the path to a file or directory in the bundled example data

    The package ships the output of a few TICRA Tools models, which
    are handy for tutorials and tests. Pass the components of the
    path relative to the data directory, e.g.::

        example_data_path("TICRA-models", "simple", "working", "polar_spherical.cut")

    Call ``example_data_path()`` without arguments to get the data
    directory itself.
    """
    resource = files("waveport").joinpath("data", *parts)
    if not isinstance(resource, Path):
        raise TypeError("Example data must be installed on the filesystem")
    return resource
