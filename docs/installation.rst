Installation
============

WavePort requires Python 3.11 or later and NumPy. Install it with pip:

.. code-block:: console

   python -m pip install waveport

For a checkout of this repository:

.. code-block:: console

   git clone https://github.com/unimilab/waveport.git
   cd waveport
   uv sync

Building from source requires a C++20 compiler and CMake. The build backend
installs its Python build dependencies, including scikit-build-core and
nanobind. CMake downloads fast_float, so a source build needs network access.

To build only the documentation, follow :doc:`contributing`; a compiler and
an installed WavePort package are not required for that build.
