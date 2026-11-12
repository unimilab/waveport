"""Sphinx configuration for WavePort."""

import re
import tomllib
from pathlib import Path

with (Path(__file__).resolve().parents[1] / "pyproject.toml").open("rb") as stream:
    metadata = tomllib.load(stream)["project"]

project = "WavePort"
author = ", ".join(person["name"] for person in metadata["authors"])
copyright = f"2026, {author}"
release = metadata["version"]
version = release

extensions = ["sphinx.ext.autodoc", "sphinx.ext.githubpages"]
root_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
nitpicky = True

html_theme = "alabaster"
html_title = f"{project} {release} documentation"
html_logo = "../logo/waveport-logo.svg"
html_theme_options = {
    "github_user": "unimilab",
    "github_repo": "waveport",
    "github_button": True,
}

# -- API reference -------------------------------------------------------------
#
# The pages in ``reference/`` use autodoc, so the package (including its
# compiled extension) must be importable when the documentation is built.

autodoc_member_order = "bysource"
autodoc_typehints = "signature"

# External types are not cross-referenced through intersphinx, so that the
# documentation can be built offline.
nitpick_ignore = [("py:class", "numpy.ndarray"), ("py:class", "pathlib.Path")]


_NANOBIND_SIGNATURE = re.compile(r"^\(self\) -> (?P<type>.+)$")


def _fix_nanobind_docstring(app, what, name, obj, options, lines) -> None:
    # Properties without an explicit docstring inherit the signature that
    # nanobind generates for their getter, e.g. ``(self) -> numpy.ndarray[...]``.
    # That is not valid reStructuredText, so render it as a literal type.
    text = [line for line in lines if line.strip()]
    if what in ("attribute", "property") and len(text) == 1:
        match = _NANOBIND_SIGNATURE.match(text[0])
        if match:
            lines[:] = [f"Type: ``{match['type']}``"]


def setup(app):
    app.connect("autodoc-process-docstring", _fix_nanobind_docstring)
