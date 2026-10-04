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

#ifndef __CUTS_HPP__
#define __CUTS_HPP__

#include "text_cursor.hpp"

#include <complex>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

enum class CutType {
  PolarSphericalCut,
  ConicalSphericalCut,
  RadialPlanarCut,
  CircularPlanarCut,
  RadialSurfaceCut,
  CircularSurfaceCut,
  AxialCylindricalCut,
  CircularCylindricalCut,
};

enum class CutGeometry {
  Spherical,
  Planar,
  Surface,
  Cylindrical,
};

enum class CutMode {
  FixedAzimuth = 1,   // ICUT=1: φ is constant
  VaryingAzimuth = 2, // ICUT=2: φ varies
};

class Cut {
public:
  using Coefficient = std::complex<double>;

  explicit Cut(TextCursor &cursor,
               std::optional<CutGeometry> geometry = std::nullopt)
      : _geometry{geometry} {
    parse_cut_file(cursor);
    validate();
  }

  [[nodiscard]]
  std::optional<CutGeometry> geometry() const noexcept {
    return _geometry;
  }

  [[nodiscard]]
  CutMode mode() const noexcept {
    return _mode;
  }

  [[nodiscard]]
  std::optional<CutType> type() const noexcept {
    if (!_geometry)
      return std::nullopt;

    const bool is_fixed = (_mode == CutMode::FixedAzimuth);

    switch (*_geometry) {
    case CutGeometry::Spherical:
      return is_fixed ? CutType::PolarSphericalCut
                      : CutType::ConicalSphericalCut;

    case CutGeometry::Planar:
      return is_fixed ? CutType::RadialPlanarCut : CutType::CircularPlanarCut;

    case CutGeometry::Surface:
      return is_fixed ? CutType::RadialSurfaceCut : CutType::CircularSurfaceCut;

    case CutGeometry::Cylindrical:
      return is_fixed ? CutType::AxialCylindricalCut
                      : CutType::CircularCylindricalCut;
    }

    return std::nullopt;
  }

  [[nodiscard]]
  std::size_t sample_count() const noexcept {
    return _sample_count;
  }

  [[nodiscard]]
  std::size_t component_count() const noexcept {
    return _component_count;
  }

  [[nodiscard]]
  const Coefficient *coefficients_data() const noexcept {
    return _coefficients.data();
  }

  [[nodiscard]]
  const Coefficient &coefficient(std::size_t sample,
                                 std::size_t component) const {
    return _coefficients.at(sample * _component_count + component);
  }

private:
  std::optional<CutGeometry> _geometry;
  CutMode _mode{};
  std::size_t _sample_count{};
  std::size_t _component_count{};
  std::vector<Coefficient> _coefficients;

  void parse_cut_file(TextCursor &cursor);
  void validate() const { /* Empty, for the moment */ }
};

using CutList = std::vector<Cut>;

#endif
