How-to guides
=============

Read a cut file from disk
-------------------------

The function :func:`waveport.load_cut` reads a ``.cut`` file and returns a :class:`.Cut` object:

.. code-block:: python

   from waveport import CutGeometry, loads_cut

   cuts = load_cut("beam_pattern.cut", geometry=CutGeometry.PLANAR)

You have to supply ``geometry`` explicitly, because TICRA cut files do not encode this information.
   
A longer, more verbose alternative is to read the file as text and
pass its contents to :func:`.loads_cut`:

.. code-block:: python

   from pathlib import Path
   from waveport import CutGeometry, loads_cut

   contents = Path("measurement.cut").read_text()
   cuts = loads_cut(contents, geometry=CutGeometry.PLANAR)


Read a grid file
----------------

The function :func:`waveport.load_grid` reads a ``.grd`` file and
returns a list of :class:`.Grid` objects:

.. code-block:: python

   from waveport import load_grid, GridGeometry

   grids = load_grid(
       "measurement.grd",
       geometry=GridGeometry.SPHERICAL,
   )
   print(f"{len(grids)} frequencies found in the file")

   for grid in grids:
       print(grid.frequency_hz, grid.coefficients.shape)


You have to supply ``geometry`` explicitly, because TICRA cut files do not encode this information.

If you want, you can read the contents of the text file and pass the
string to :func:`.loads_grid`.


Read SWE coefficients
---------------------

The function :func:`waveport.load_swe` reads a ``.sph`` file and
returns a list of :class:`.Swe` objects:

.. code-block:: python

   from waveport import load_swe

   swe_list = load_grid("measurement_swe.sph")
   print(f"{len(swe_list)} frequencies found in the file")

   for swe in swe_list:
       print(swe.frequency_hz, swe.num_of_coefficients)


If you want, you can read the contents of the text file and pass the
string to :func:`.loads_swe`.


Handle invalid input
--------------------

.. code-block:: python

   from waveport import ParseError, loads_cut

   try:
       # These surely are not the contents of a valid .cut file!
       cuts = loads_cut("invalid file contents")
   except ParseError as error:
       print(f"Could not read the cut: {error}")
