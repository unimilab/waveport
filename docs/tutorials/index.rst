Tutorial: read a field cut
==============================

This example reads a bundled spherical cut file, then inspects its field
coefficients. Run it in an environment with WavePort installed.

.. code-block:: python

   import numpy as np
   from waveport import example_data_path, loads_cut

   cuts = load_cut(example_data_path("spherical_polar.cut"))
   first_cut = cuts[0]

   print(first_cut.num_of_values_in_cut)
   print(first_cut.coefficients.shape)
   amplitude = np.abs(first_cut.coefficients)

A file can contain multiple cuts, so :func:`waveport.loads_cut` returns a list.
Each cut's coefficient array has one row per sample and one column per field
component. ``amplitude`` contains the absolute values of the complex fields.
