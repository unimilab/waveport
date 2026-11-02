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

#include "grids.hpp"
#include "fast_float/fast_float.h"
#include "parse_numbers.hpp"
#include "text_cursor.hpp"

#include <exception>
#include <format>
#include <limits> // For std::numeric_limits<double>::quiet_NaN()
#include <sstream>
#include <utility>

static std::vector<double>
read_frequencies_from_grid_header(std::vector<std::string_view> lines) {

  /* This might not be the fastest implementation possible, but keep
   * in mind that we are dealing with only a few lines in a
   * potentially *huge* file: the bottleneck in performance is surely
   * not caused by the header parsing routine! */

  if (lines.empty())
    throw ParseError("Empty grid header");

  size_t cur_line_idx{};
  std::vector<double> frequencies_hz;

  while (cur_line_idx < lines.size()) {
    std::string_view cur_line{lines.at(cur_line_idx)};

    if (cur_line.starts_with("FREQUENCIES")) {
      /* This line and the following are of the form
       *
       *    FREQUENCIES [GHz]:
       *      0.1000000000E+02  0.1500000000E+02  0.2000000000E+02
       *
       * We must:
       *
       * 1. Parse the measurement unit
       * 2. Count and read each of the frequencies and save them in
       *    `frequencies_hz`
       */
      auto freq_line{lines.at(cur_line_idx)};

      ////////////////////////////////////////////////////////////
      // Read the measurement unit in `cur_line`

      size_t unit_start{cur_line.find('[')};
      // We start from 1 because we must skip the opening '['
      size_t unit_end{cur_line.find(']', unit_start)};

      if (unit_end - 1 == unit_start)
        throw ParseError(
            "Missing measurement unit for frequencies in grid header");

      std::string_view measurement_unit{
          cur_line.substr(unit_start + 1, (unit_end - unit_start) - 1)};

      double unit_factor{};
      if (measurement_unit == "GHz") {
        unit_factor = 1e9;
      } else if (measurement_unit == "MHz") {
        unit_factor = 1e6;
      } else if (measurement_unit == "KHz") {
        unit_factor = 1e3;
      } else if (measurement_unit == "Hz") {
        unit_factor = 1.0;
      } else {
        throw ParseError(std::format(
            "Unknown measurement unit \"{}\" for frequencies in grid header",
            measurement_unit));
      }

      ////////////////////////////////////////////////////////////
      // Read the list of frequencies from `freq_line`
      auto freq_list_line{lines.at(++cur_line_idx)};
      std::stringstream freq_line_stream{
          std::move(std::string(freq_list_line))};

      while (freq_line_stream.good()) {
        double cur_frequency;
        freq_line_stream >> cur_frequency;
        frequencies_hz.push_back(cur_frequency * unit_factor);
      }
    }

    cur_line_idx++;
  }

  return frequencies_hz;
}

void Grid::read_implicit_coefficients(
    TextCursor &cursor, Grid &cur_grid,
    std::span<std::complex<double>> &coefficients, size_t nx, size_t ny,
    GridList &result) {
  /* The TICRA User’s manual is not super-clear about how the
   * “implicit” scheme (KLIMIT=1) works, so here is a practical example.
   *
   * The contents of the file are the following:
   *
   *        7    1
   *    [one complex number: real + imaginary part]
   *        4    7
   *    [seven complex numbers: real + imaginary part]
   *        3    9
   *    [nine complex numbers: real + imaginary part]
   *
   * and so on. The pair of integers are the IS,IN numbers, and they
   * specify which part of the current row should be filled. Any value
   * outside of this range should be considered “missing”, i.e, what
   * GNU R identifies as `NA` and Julia interprets as `Nothing`. In
   * Python we could use masked arrays, as they are designed exactly
   * for this purpose, but this would make the API return a different
   * type of array (either a plain NumPy array or a masked array)
   * depending on the file type. WavePort instead fills the missing
   * values with `NaN`, as this value cannot be found in TICRA files
   * and thus leaves no ambiguity. For those who really need a masked
   * array, it is trivial to do the conversion.
   *
   * Here is a visual representation of the grid in the examplefile
   * `planar_rho_phi.grd`, which uses the KLIMIT=1 scheme:
   *
   *        1   2   3   4   5   6   7   8   9   10  11  12  13    IS,IN
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    1 |   |   |   |   |   |   | X |   |   |   |   |   |   |    7,1
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    2 |   |   |   | X | X | X | X | X | X | X |   |   |   |    4,7
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    3 |   |   | X | X | X | X | X | X | X | X | X |   |   |    3,9
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    4 |   | X | X | X | X | X | X | X | X | X | X | X |   |   2,11
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    5 |   | X | X | X | X | X | X | X | X | X | X | X |   |   2,11
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    6 | X | X | X | X | X | X | X | X | X | X | X | X | X |   1,13
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    7 |   | X | X | X | X | X | X | X | X | X | X | X |   |   2,11
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    8 |   | X | X | X | X | X | X | X | X | X | X | X |   |   2,11
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *    9 |   |   | X | X | X | X | X | X | X | X | X |   |   |    3,9
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *   10 |   |   |   | X | X | X | X | X | X | X |   |   |   |    4,7
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   *   11 |   |   |   |   |   |   | X |   |   |   |   |   |   |    7,1
   *      +---+---+---+---+---+---+---+---+---+---+---+---+---+
   */

  // Now parse the file
  for (size_t cur_row{}; cur_row < ny; ++cur_row) {
    auto cur_line{cursor.read_line()};
    if (!cur_line.has_value())
      throw ParseError("Incomplete data in grid");

    // Read IS, IN
    auto [start_column,
          num_of_columns]{parse_numbers<size_t, size_t>(*cur_line)};

    size_t first_elem_in_row_idx = cur_row * nx * cur_grid._component_count;
    size_t idx;

    // Set to NaN the first part of the row
    for (idx = first_elem_in_row_idx;
         idx < first_elem_in_row_idx + start_column * cur_grid._component_count;
         ++idx) {
      coefficients[idx] =
          std::complex<double>(std::numeric_limits<double>::quiet_NaN(),
                               std::numeric_limits<double>::quiet_NaN());
    }

    // Fill the middle part of the row with the actual numbers read from the
    // file
    for (size_t component_idx{}; component_idx < num_of_columns;
         ++component_idx) {
      cursor.read_numeric_line(coefficients.subspan(
          first_elem_in_row_idx +
              (start_column + component_idx - 1) * cur_grid._component_count,
          cur_grid._component_count));
    }

    // Fill the tail of the row with NaNs
    for (idx = first_elem_in_row_idx +
               (start_column + num_of_columns - 1) * cur_grid._component_count;
         idx < (cur_row + 1) * nx * cur_grid._component_count; ++idx) {
      coefficients[idx] =
          std::complex<double>(std::numeric_limits<double>::quiet_NaN(),
                               std::numeric_limits<double>::quiet_NaN());
    }
  }
}

void Grid::read_explicit_coefficients(
    TextCursor &cursor, Grid &cur_grid,
    std::span<std::complex<double>> &coefficients, size_t nx, size_t ny,
    GridList &result) {
  size_t num_of_values{nx * ny};
  for (size_t i{}; i < num_of_values; ++i) {
    cursor.read_numeric_line(coefficients.subspan(i * cur_grid._component_count,
                                                  cur_grid._component_count));
  }

  result.emplace_back(cur_grid);
}

GridList Grid::parse_grid_file(TextCursor &cursor,
                               std::optional<GridGeometry> geometry) {
  GridList result;

  ////////////////////////////////////////////////////////////
  // Read the header and store it in `header_lines`

  std::vector<std::string_view> header_lines;
  while (true) {
    auto cur_line{cursor.read_line()};

    if (!cur_line.has_value())
      throw ParseError("Unexpected end of file while reading the grid header");

    if ((*cur_line).starts_with("++++"))
      break;

    header_lines.push_back(*cur_line);
  }
  std::vector<double> frequencies_hz{
      read_frequencies_from_grid_header(header_lines)};

  ////////////////////////////////////////////////////////////
  // Read the integer parameters at the beginning of the file

  auto cur_line{cursor.read_line()};
  if (!cur_line.has_value())
    throw ParseError("Unexpected end of file while reading the grid header");
  auto [ktype]{parse_numbers<int>(*cur_line)};

  if (!(ktype == 1))
    throw ParseError(
        std::format("Unexpected value KTYPE={} in grid file", ktype));

  cur_line = cursor.read_line();
  if (!cur_line.has_value())
    throw ParseError("Unexpected end of file while reading the grid header");
  auto [nset, icomp, ncomp,
        igrid]{parse_numbers<size_t, int, int, int>(*cur_line)};

  if (!frequencies_hz.empty() && nset != frequencies_hz.size())
    throw ParseError(
        std::format("Mismatch in the number of frequencies ({}) and NSET={}",
                    frequencies_hz.size(), nset));

  ////////////////////////////////////////////////////////////
  // Read the centers of the set of beams

  std::vector<std::pair<int, int>> centers;

  for (size_t i{}; i < nset; ++i) {
    auto cur_line{cursor.read_line()};
    if (!cur_line.has_value())
      throw ParseError(
          "Unexpected end of file while parsing centers in grid file");

    auto [ix, iy]{parse_numbers<int, int>(*cur_line)};
    centers.push_back(std::make_pair(ix, iy));
  }

  // The following is repeated NSET times (one per frequency)
  for (size_t cur_set{}; cur_set < nset; ++cur_set) {
    Grid cur_grid{geometry};
    cur_grid._frequency_hz = frequencies_hz.at(cur_set);
    cur_grid._component_type = static_cast<ComponentType>(icomp);
    cur_grid._component_count = static_cast<std::size_t>(ncomp);
    cur_grid._grid_type = static_cast<GridType>(igrid);
    cur_grid._center_x = centers[cur_set].first;
    cur_grid._center_y = centers[cur_set].second;

    ////////////////////////////////////////////////////////////
    // Read the extents of the grid
    auto cur_line{cursor.read_line()};
    if (!cur_line.has_value())
      throw ParseError(std::format(
          "Unexpected end of file while parsing the extents of grid #{}/{}",
          cur_set + 1, ncomp));

    auto [xs, ys, xe,
          ye]{parse_numbers<double, double, double, double>(*cur_line)};
    cur_grid._start_x = xs;
    cur_grid._start_y = ys;
    cur_grid._end_x = xe;
    cur_grid._end_y = ye;

    ////////////////////////////////////////////////////////////
    // Read the size of the grid
    cur_line = cursor.read_line();
    if (!cur_line.has_value())
      throw ParseError(std::format(
          "Unexpected end of file while parsing the size of grid #{}/{}",
          cur_set + 1, ncomp));
    auto [nx, ny, klimit]{parse_numbers<size_t, size_t, int>(*cur_line)};
    cur_grid._num_of_x = nx;
    cur_grid._num_of_y = ny;

    ////////////////////////////////////////////////////////////
    // Read the coefficients

    try {
      cur_grid._coefficients.resize(nx * ny * cur_grid._component_count);
      std::span<std::complex<double>> coefficients{cur_grid._coefficients};

      switch (klimit) {
      case 0:
        read_explicit_coefficients(cursor, cur_grid, coefficients, nx, ny,
                                   result);
        break;
      case 1:
        read_implicit_coefficients(cursor, cur_grid, coefficients, nx, ny,
                                   result);
        break;
      default:
        throw ParseError(
            std::format("Currently WavePort only supports KLIMIT=0,1 "
                        "grid files, but here KLIMIT={}",
                        klimit));
      }
    } catch (const std::runtime_error &err) {
      // Convert any std::runtime_error raised by
      // `TextCursor::read_numeric_line` into a proper `ParserError`, including
      // the current line number
      throw ParseError(std::format("Error at line {}: {}", cursor.line_number(),
                                   err.what()));
    }

    result.emplace_back(cur_grid);
  }

  return result;
}
