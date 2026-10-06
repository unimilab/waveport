# -*- encoding: utf-8 -*-
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
from importlib.resources.abc import Traversable

def example_data_path(*parts: str) -> Traversable:
    """Return the path to a file or directory in the bundled example data

    The package ships the output of a few TICRA Tools models, which
    are handy for tutorials and tests. Pass the components of the
    path relative to the data directory, e.g.::

        example_data_path("TICRA-models", "simple", "working", "polar_spherical.cut")

    Call ``example_data_path()`` without arguments to get the data
    directory itself.
    """
    return files(__package__).joinpath("data", *parts)
