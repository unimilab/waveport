"""Sphinx configuration for WavePort."""

import tomllib
from pathlib import Path

with (Path(__file__).resolve().parents[1] / "pyproject.toml").open("rb") as stream:
    metadata = tomllib.load(stream)["project"]

project = "WavePort"
author = ", ".join(person["name"] for person in metadata["authors"])
copyright = f"2026, {author}"
release = metadata["version"]
version = release

extensions = ["sphinx.ext.githubpages"]
root_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
nitpicky = True

html_theme = "alabaster"
html_title = f"{project} {release} documentation"
html_logo = "../logo/waveport-logo.svg"
html_theme_options = {
    "github_user": "ziotom78",
    "github_repo": "waveport",
    "github_button": True,
}
