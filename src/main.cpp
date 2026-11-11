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

#include <format>

#include "cuts.hpp"
#include "grids.hpp"
#include "parse_numbers.hpp"
#include "swe.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/complex.h>
#include <nanobind/stl/optional.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/string_view.h>
#include <nanobind/stl/vector.h>

namespace nb = nanobind;

////////////////////////////////////////////////////////////
// Cuts

CutList loads_cut(std::string_view contents,
                  std::optional<CutGeometry> geometry = std::nullopt) {
  TextCursor cursor{contents};
  CutList cuts;

  while (!cursor.at_end()) {
    cuts.emplace_back(cursor, geometry);
  }
  return cuts;
}

////////////////////////////////////////////////////////////
// Grids

GridList loads_grid(std::string_view contents,
                    std::optional<GridGeometry> geometry = std::nullopt) {
  TextCursor cursor{contents};
  return Grid::parse_grid_file(cursor, geometry);
}

////////////////////////////////////////////////////////////
// SWEs

SweList loads_swe(std::string_view contents) {
  TextCursor cursor{contents};
  return Swe::parse_swe_file(cursor);
}

////////////////////////////////////////////////////////////
// Main

using CoefficientArray = nb::ndarray<nb::numpy, const std::complex<double>,
                                     nb::ndim<2>, nb::c_contig>;

NB_MODULE(_core, m) {
  nb::exception<ParseError>(m, "ParseError", PyExc_ValueError);

  nb::enum_<ComponentType>(m, "ComponentType")
      .value("LINEAR_THETA_PHI", ComponentType::LinearThetaPhi)
      .value("CIRCULAR", ComponentType::Circular)
      .value("CO_CROSS", ComponentType::CoCross)
      .value("LINEAR_ALONG_POL_ELLIPSE", ComponentType::LinearAlongPolEllipse)
      .value("XPD_THETA_PHI", ComponentType::XPDThetaPhi)
      .value("XPD_CIRCULAR", ComponentType::XPDCircular)
      .value("XPD_CO_CROSS", ComponentType::XPDCoCross)
      .value("XPD_POL_ELLIPSE", ComponentType::XPDPolEllipse)
      .value("TOTAL_POWER_AND_CIRCULAR_RATIO",
             ComponentType::TotalPowerAndCircularRatio)
      .value("POYNTING_VECTOR", ComponentType::PoyntingVector);

  //////////////////////////////////////////////////
  // Cuts

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
    return std::format("Cut(geometry={}, mode={})",
                       nb::str(nb::cast(cut.geometry())).c_str(),
                       nb::str(nb::cast(cut.mode())).c_str());
  });

  m.def("loads_cut", loads_cut, nb::arg("contents"),
        nb::arg("geometry") = nb::none());

  //////////////////////////////////////////////////
  // Grids

  nb::enum_<GridGeometry>(m, "GridGeometry")
      .value("SPHERICAL", GridGeometry::Spherical)
      .value("PLANAR", GridGeometry::Planar)
      .value("SURFACE", GridGeometry::Surface)
      .value("CYLINDRICAL", GridGeometry::Cylindrical);

  nb::enum_<GridType>(m, "GridType")
      .value("UV", GridType::UV)
      .value("RHO_PHI", GridType::RhoPhi)
      .value("XY", GridType::XY)
      .value("ELEVATION_OVER_AZIMUTH", GridType::ElevationOverAzimuth)
      .value("ELEVATION_AND_AZIMUTH", GridType::ElevationAndAzimuth)
      .value("AZIMUTH_OVER_ELEVATION", GridType::AzimuthOverElevation)
      .value("THETA_PHI", GridType::ThetaPhi)
      .value("PHI_Z", GridType::PhiZ)
      .value("AZIMUTH_OVER_ELEVATION_EDX", GridType::AzimuthOverElevationEDX)
      .value("ELEVATION_OVER_AZIMUTH_EDX", GridType::ElevationOverAzimuthEDX);

  auto grid_class{nb::class_<Grid>(m, "Grid")};

  grid_class.def_prop_ro("geometry", &Grid::geometry)
      .def_prop_ro("frequency_hz", &Grid::frequency_hz)
      .def_prop_ro("x_vector", &Grid::x_vector)
      .def_prop_ro("y_vector", &Grid::y_vector)
      .def_prop_ro("grid_type", &Grid::grid_type)
      .def_prop_ro("num_of_values_along_x", &Grid::num_of_values_along_x)
      .def_prop_ro("num_of_values_along_y", &Grid::num_of_values_along_y)
      .def_prop_ro("component_type", &Grid::component_type)
      .def_prop_ro("component_count", &Grid::component_count)
      .def_prop_ro(
          "coefficients",
          [](const Grid &grid) {
            return CoefficientArray{grid.coefficients_data(),
                                    {grid.num_of_values_along_y(),
                                     grid.num_of_values_along_x(),
                                     grid.component_count()}};
          },
          nb::rv_policy::reference_internal);

  grid_class.def("__repr__", [](const Grid &grid) {
    return std::format("Grid(geometry={})",
                       nb::str(nb::cast(grid.geometry())).c_str());
  });

  m.def("loads_grid", loads_grid, nb::arg("contents"),
        nb::arg("geometry") = nb::none());

  //////////////////////////////////////////////////
  // SWEs

  auto swe_class{nb::class_<Swe>(m, "Swe")};

  swe_class.def_prop_ro("frequency_hz", &Swe::frequency_hz)
      .def_prop_ro("num_of_theta", &Swe::num_of_theta)
      .def_prop_ro("num_of_phi", &Swe::num_of_phi)
      .def_prop_ro("n_max", &Swe::n_max)
      .def_prop_ro("m_max", &Swe::m_max)
      .def_prop_ro("cum_power_w", &Swe::cum_power_w);

  swe_class.def("are_indexes_valid", &Swe::are_indexes_valid, nb::arg("s"),
                nb::arg("m"), nb::arg("n"));
  swe_class.def("coefficient", &Swe::coefficient, nb::arg("s"), nb::arg("m"),
                nb::arg("n"));

  swe_class.def("__repr__", [](const Swe &swe) {
    return std::format("Swe(mmax={}, nmax={})", swe.m_max(), swe.n_max());
  });

  m.def("loads_swe", loads_swe, nb::arg("contents"));
}
