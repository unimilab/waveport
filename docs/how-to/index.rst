How-to guides
=============

Read a cut file from disk
-------------------------

Read the file as text and pass its contents to :func:`waveport.loads_cut`:

.. code-block:: python

   from pathlib import Path
   from waveport import CutGeometry, loads_cut

   contents = Path("measurement.cut").read_text()
   cuts = loads_cut(contents, geometry=CutGeometry.PLANAR)

Supply ``geometry`` when the file's cut codes are ambiguous; see
:doc:`../explanation/index`.

Read a grid file
----------------

.. code-block:: python

   from pathlib import Path
   from waveport import loads_grid

   grids = loads_grid(Path("measurement.grd").read_text())
   for grid in grids:
       print(grid.frequency_hz, grid.coefficients.shape)

Handle invalid input
--------------------

.. code-block:: python

   from waveport import ParseError, loads_cut

   try:
       cuts = loads_cut("invalid file contents")
   except ParseError as error:
       print(f"Could not read the cut: {error}")
