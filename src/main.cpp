/* -*- encoding: utf-8 -*-
 *
 * ***           **             **************
 * ****          ***         ********************
 *  ***         ****         ********      ******
 *  ***         ****        *****             ****
 *  ***         *****       ***                  **
 *   ***       ******       **                ** **
 *   ***       ******      **             *********
 *    **       **  **      **          ************
 *    ***     **   ***     *         *************
 *     **     **    **    **    *****************
 *     ***   ***    ***   **   *****************
 *      *******     *******    *************
 *      ******       ******    ***
 *       *****        ****     ***
 *        ***          ***     ***
 *
 * WavePort — A Python library for reading TICRA Tools files
 *
 * Licensed under the GNU General Public License 3 or later.
 * See the file LICENSE.txt
 *
 * Copyright © 2026 Maurizio Tomasi
 */

#include "fast_float/fast_float.h"
#include <format>

#include "cuts.hpp"
#include "parse_numbers.hpp"
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/string_view.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;

CutList loads_cut(std::string_view contents,
                  std::optional<CutGeometry> geometry = std::nullopt) {
  TextCursor cursor{contents};
  CutList cuts;

  while (!cursor.at_end()) {
    cuts.emplace_back(cursor, geometry);
  }
  return cuts;
}

using CoefficientArray = nb::ndarray<nb::numpy, const std::complex<double>,
                                     nb::ndim<2>, nb::c_contig>;

NB_MODULE(_core, m) {
  nb::exception<ParseError>(m, "ParseError", PyExc_ValueError);

  nb::enum_<CutGeometry>(m, "CutGeometry")
      .value("SPHERICAL", CutGeometry::Spherical)
      .value("PLANAR", CutGeometry::Planar)
      .value("SURFACE", CutGeometry::Surface)
      .value("CYLINDRICAL", CutGeometry::Cylindrical);

  nb::enum_<CutMode>(m, "CutMode")
      .value("FIXED_AZIMUTH", CutMode::FixedAzimuth)
      .value("VARYING_AZIMUTH", CutMode::VaryingAzimuth);

  nb::enum_<CutType>(m, "CutType")
      .value("POLAR_SPHERICAL", CutType::PolarSphericalCut)
      .value("CONICAL_SPHERICAL", CutType::ConicalSphericalCut)
      .value("RADIAL_PLANAR", CutType::RadialPlanarCut)
      .value("CIRCULAR_PLANAR", CutType::CircularPlanarCut)
      .value("RADIAL_SURFACE", CutType::RadialSurfaceCut)
      .value("CIRCULAR_SURFACE", CutType::CircularSurfaceCut)
      .value("AXIAL_CYLINDRICAL", CutType::AxialCylindricalCut)
      .value("CIRCULAR_CYLINDRICAL", CutType::CircularCylindricalCut);

  auto cut_class{nb::class_<Cut>(m, "Cut")};

  cut_class.def_prop_ro("geometry", &Cut::geometry)
      .def_prop_ro("mode", &Cut::mode)
      .def_prop_ro("type", &Cut::type)
      .def_prop_ro("init_value", &Cut::init_value)
      .def_prop_ro("increment", &Cut::increment)
      .def_prop_ro("constant_angle", &Cut::constant_angle)
      .def_prop_ro("num_of_values_in_cut", &Cut::num_of_values_in_cut)
      .def_prop_ro("component_count", &Cut::component_count)
      .def_prop_ro(
          "coefficients",
          [](const Cut &cut) {
            return CoefficientArray{
                cut.coefficients_data(),
                {cut.num_of_values_in_cut(), cut.component_count()}};
          },
          nb::rv_policy::reference_internal);

  cut_class.def("__repr__", [](const Cut &cut) {
    // Converting to Python objects gives "CutGeometry.SPHERICAL",
    // "None", etc., consistent with the names exposed above
    return std::format("Cut(geometry={}, mode={})",
                       nb::str(nb::cast(cut.geometry())).c_str(),
                       nb::str(nb::cast(cut.mode())).c_str());
  });

  m.def("loads_cut", loads_cut, nb::arg("contents"),
        nb::arg("geometry") = nb::none());
}
