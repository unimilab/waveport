API reference
=============

The following objects are exposed by ``waveport``. The reference is written
with Sphinx's Python domain so it can be built without importing the native
extension. Keep signatures aligned with ``src/waveport/_core.pyi`` and the
extension bindings when changing the API.

.. py:currentmodule:: waveport

Parsers
-------

.. py:function:: loads_cut(contents, geometry=None)

   Parse the text of a TICRA cut file and return a list of :class:`Cut` objects.
   ``geometry`` accepts a :class:`CutGeometry` value or ``None``.
   Raise :exc:`ParseError` for invalid input.

.. py:function:: loads_grid(contents, geometry=None)

   Parse the text of a TICRA grid file and return a list of :class:`Grid`
   objects. ``geometry`` accepts a :class:`GridGeometry` value or ``None``.
   Raise :exc:`ParseError` for invalid input.

Data containers
---------------

.. py:class:: Cut

   A parsed cut. Read-only properties include ``geometry``, ``mode``, ``type``,
   ``init_value``, ``increment``, ``constant_angle``, ``num_of_values_in_cut``,
   ``component_count``, and ``coefficients``. The complex coefficient array has
   shape ``(num_of_values_in_cut, component_count)``.

.. py:class:: Grid

   A parsed grid. Read-only properties include ``geometry``, ``frequency_hz``,
   ``x_vector``, ``y_vector``, ``grid_type``, ``num_of_values_along_x``,
   ``num_of_values_along_y``, ``component_type``, ``component_count``, and
   ``coefficients``. See :doc:`../explanation/index` for array dimensions.

Enumerations
------------

.. py:class:: CutGeometry

   ``SPHERICAL``, ``PLANAR``, ``SURFACE``, and ``CYLINDRICAL``.

.. py:class:: GridGeometry

   ``SPHERICAL``, ``PLANAR``, ``SURFACE``, and ``CYLINDRICAL``.

.. py:class:: CutMode

   ``FIXED_AZIMUTH`` and ``VARYING_AZIMUTH``.

.. py:class:: CutType

   ``POLAR_SPHERICAL``, ``CONICAL_SPHERICAL``, ``RADIAL_PLANAR``,
   ``CIRCULAR_PLANAR``, ``RADIAL_SURFACE``, ``CIRCULAR_SURFACE``,
   ``AXIAL_CYLINDRICAL``, and ``CIRCULAR_CYLINDRICAL``.

.. py:class:: GridType

   ``UV``, ``RHO_PHI``, ``XY``, ``ELEVATION_OVER_AZIMUTH``,
   ``ELEVATION_AND_AZIMUTH``, ``AZIMUTH_OVER_ELEVATION``, ``THETA_PHI``,
   ``PHI_Z``, ``AZIMUTH_OVER_ELEVATION_EDX``, and ``ELEVATION_OVER_AZIMUTH_EDX``.

.. py:class:: ComponentType

   Field component representations: ``LINEAR_THETA_PHI``, ``CIRCULAR``,
   ``CO_CROSS``, ``LINEAR_ALONG_POL_ELLIPSE``, ``XPD_THETA_PHI``,
   ``XPD_CIRCULAR``, ``XPD_CO_CROSS``, ``XPD_POL_ELLIPSE``,
   ``TOTAL_POWER_AND_CIRCULAR_RATIO``, and ``POYNTING_VECTOR``.

Errors and example data
-----------------------

.. py:exception:: ParseError

   A subclass of ``ValueError`` raised when input cannot be parsed.

.. py:function:: example_data_path(*parts)

   Return an ``importlib.resources.abc.Traversable`` for a path relative to the
   bundled example data. Call ``read_text()`` to read a sample, or omit
   ``parts`` to access the data directory.
