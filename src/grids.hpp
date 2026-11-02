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

#ifndef __GRIDS_HPP__
#define __GRIDS_HPP__

#include "component_type.hpp"
#include "text_cursor.hpp"

#include <complex>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

enum class GridGeometry {
  Spherical,
  Planar,
  Surface,
  Cylindrical,
};

enum class GridType {
  UV = 1,
  RhoPhi = 2,
  XY = 3,
  ElevationOverAzimuth = 4,
  ElevationAndAzimuth = 5,
  AzimuthOverElevation = 6,
  ThetaPhi = 7,
  PhiZ = 8,
  AzimuthOverElevationEDX = 9,
  ElevationOverAzimuthEDX = 10,
};

/* The logic used to load grid files is different from the one used
 * for cut files. The problem is that, unlike `.cut` files, `.grd`
 * files have a shared header that specifies a number of properties
 * that apply to each of the frequencies listed in the `.grd` file.
 * Thus, we must parse all the frequencies at the same time, instead
 * of reading them one by one as we do for `.cut` files.
 *
 * We duplicate all the information in the header in each `Grid`
 * instance, so that from the point of view of the high-level
 * interface, everything works as for `Cut` objects.
 */

class Grid;
using GridList = std::vector<Grid>;

class Grid {
public:
  using Coefficient = std::complex<double>;

  explicit Grid(std::optional<GridGeometry> geometry = std::nullopt)
      : _geometry{geometry} {}

  [[nodiscard]]
  std::optional<GridGeometry> geometry() const noexcept {
    return _geometry;
  }

  [[nodiscard]]
  double frequency_hz() const noexcept {
    return _frequency_hz;
  }

  [[nodiscard]]
  std::vector<double> x_vector() const noexcept {
    return get_vector_of_points(_start_x, _end_x, _num_of_x, _center_x);
  }

  [[nodiscard]]
  std::vector<double> y_vector() const noexcept {
    return get_vector_of_points(_start_y, _end_y, _num_of_y, _center_y);
  }

  [[nodiscard]]
  GridType grid_type() const noexcept {
    return _grid_type;
  }

  [[nodiscard]]
  ComponentType component_type() const noexcept {
    return _component_type;
  }

  /** \brief Number of components of each sample of the electric field
   *
   * It can either be 2 (far field) or 3 (near field).
   */
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

  static GridList
  parse_grid_file(TextCursor &cursor,
                  std::optional<GridGeometry> geometry = std::nullopt);

private:
  std::optional<GridGeometry> _geometry{};
  GridType _grid_type{};
  ComponentType _component_type{};
  std::size_t _component_count{}; // Either 2 (far field) or 3 (near field)
  double _frequency_hz;
  int _center_x, _center_y;
  double _start_x, _end_x;
  double _start_y, _end_y;
  size_t _num_of_x, _num_of_y;
  std::vector<Coefficient> _coefficients;

  static void
  read_implicit_coefficients(TextCursor &cursor, Grid &cur_grid,
                             std::span<std::complex<double>> &coefficients,
                             size_t nx, size_t ny, GridList &result);

  static void
  read_explicit_coefficients(TextCursor &cursor, Grid &cur_grid,
                             std::span<std::complex<double>> &coefficients,
                             size_t nx, size_t ny, GridList &result);

  [[nodiscard]]
  static std::vector<double> get_vector_of_points(double start, double end,
                                                  size_t num,
                                                  int center_idx) noexcept {
    double delta{(end - start) / (num - 1)};
    double center{delta * center_idx};

    std::vector<double> result(num);
    for (size_t i{}; i < num; ++i) {
      result[i] = center + start + delta * i;
    }

    return result;
  }

  void validate() const { /* Empty, for the moment */ }
};

#endif
