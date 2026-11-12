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

import bz2
import gzip
from collections.abc import Callable
from pathlib import Path
from typing import IO, Any

################################################################################
# Common stuff


def _load_text_file(f: IO, handler: Callable[[str], Any], *args, **kwargs) -> Any:
    contents = "".join(f.readlines())
    return handler(contents, *args, **kwargs)


def load_text_file_path(
    path: str | Path, handler: Callable[[str], Any], *args, **kwargs
) -> Any:
    path = Path(path)
    if path.suffix.lower() == ".gz":
        with gzip.open(path, "rt") as inpf:
            return _load_text_file(inpf, handler, *args, **kwargs)
    elif path.suffix.lower() == ".bz2":
        with bz2.open(path, "rt") as inpf:
            return _load_text_file(inpf, handler, *args, **kwargs)
    else:
        with open(path, "rt") as inpf:
            return _load_text_file(inpf, handler, *args, **kwargs)
