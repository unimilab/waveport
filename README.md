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

```python
from waveport import CutGeometry, loads_cut

cuts = load_cut("beam_pattern.cut", geometry=CutGeometry.PLANAR)
```

### Loading a `.grd` file

```python
from waveport import load_grid, GridGeometry

grids = load_grid(
    "measurement.grd",
    geometry=GridGeometry.SPHERICAL,
)
print(f"{len(grids)} frequencies found in the file")

for grid in grids:
    print(grid.frequency_hz, grid.coefficients.shape)
```

### Loading a `.swe` file

```python
from waveport import load_swe

swe_list = load_grid("measurement_swe.sph")
print(f"{len(swe_list)} frequencies found in the file")

for swe in swe_list:
    print(swe.frequency_hz, swe.num_of_coefficients)
```

## Documentation

The Sphinx documentation lives in [`docs/`](docs/index.rst) and is published at <https://unimilab.github.io/waveport/>.

You can build it locally from the repository root:

```sh
uv sync --locked --group docs
uv run --no-sync sphinx-build -M html docs docs/_build -W --keep-going
```

Open `docs/_build/html/index.html` to view the result. See the [documentation contributor guide](docs/contributing.rst) for the layout, build commands, and GitHub Pages setup.

## Development

Install the development dependencies with `uv sync`. With `prek` installed, run `prek install` once per clone to enable the commit hook. Every commit checks the whole repository with `uv run ruff format --check .`, `uv run ruff check .`, and `uv run ty check .`. Run `prek run --all-files` to run the checks manually.

## License

WavePort is released under the GPL license version 3 or later. See the file [LICENSE.txt](LICENSE.txt) for the full text of the license.
