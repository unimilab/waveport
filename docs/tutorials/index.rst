Tutorial: read a field cut
==============================

This example reads a bundled spherical cut file, then inspects its field
coefficients. Run it in an environment with WavePort installed.

.. code-block:: python

   import numpy as np
   from waveport import example_data_path, loads_cut

   contents = example_data_path("spherical_polar.cut").read_text()
   cuts = loads_cut(contents)
   first_cut = cuts[0]

   print(first_cut.num_of_values_in_cut)
   print(first_cut.coefficients.shape)
   amplitude = np.abs(first_cut.coefficients)

A file can contain multiple cuts, so :func:`waveport.loads_cut` returns a list.
Each cut's coefficient array has one row per sample and one column per field
component. ``amplitude`` contains the absolute values of the complex fields.

Continue with :doc:`../how-to/index` to read your own files and grid data.
