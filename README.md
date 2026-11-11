# WavePort: a Python package to load TICRA Tools files

![](logo/waveport-logo.svg)

This is the repository of WavePort, a Python package that loads `.cut`, `.grd`, `.swe`/`.sph`, and `.tor` files created by [TICRA Tools](https://www.ticra.com/software/ticratools/), an antenna analysis software.

Status of the implementation:

- [X] Read `.cut` files
- [X] Read `.grd` files
- [X] Read `.swe`/`.sph` files
- [ ] Read `.tor` files

## Example

### Loading a `.cut` file

### Loading a `.grd` file

### Loading a `.swe` file

## Documentation

The Sphinx documentation lives in [`docs/`](docs/index.rst) and is published at
<https://ziotom78.github.io/waveport/> once GitHub Pages is enabled.
Build it locally from the repository root:

```sh
uv sync --locked --only-group docs
uv run --no-sync sphinx-build -M html docs docs/_build -W --keep-going
```

Open `docs/_build/html/index.html` to view the result. See the
[documentation contributor guide](docs/contributing.rst) for the layout,
build commands, and GitHub Pages setup.

## Development

Install the development dependencies with `uv sync`. With `prek` installed, run
`prek install` once per clone to enable the commit hook. Every commit checks the
whole repository with `uv run ruff format --check .`, `uv run ruff check .`, and
`uv run ty check .`. Run `prek run --all-files` to run the checks manually.

## License

WavePort is released under the GPL license version 3 or later. See the file [LICENSE.txt](LICENSE.txt) for the full text of the license.
