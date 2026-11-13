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

#include "swe.hpp"
#include "parse_numbers.hpp"

#include "fast_float/fast_float.h"
#include <algorithm> // For std::max
#include <format>
#include <regex>
#include <string>

static const std::regex FREQUENCY_RE(
    R"(Freq\s*\[([^\]]+)\]:\s*([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?))");

static bool case_insensitive_compare(std::string_view a, std::string_view b) {
  if (a.size() != b.size())
    return false;

  for (size_t i{}; i < a.size(); ++i) {
    if (tolower(a[i]) != tolower(b[i]))
      return false;
  }

  return true;
}

std::optional<double> Swe::parse_frequency(std::string_view line) {

  std::cmatch m;
  if (!std::regex_search(line.data(), line.data() + line.size(), m,
                         FREQUENCY_RE))
    return std::nullopt;

  const std::string unit_str{m[1].str()};
  const std::string value_str{m[2].str()};
  double factor;
  if (case_insensitive_compare(unit_str, "GHz"))
    factor = 1e9;
  else if (case_insensitive_compare(unit_str, "MHz"))
    factor = 1e6;
  else if (case_insensitive_compare(unit_str, "KHz"))
    factor = 1e3;
  else if (case_insensitive_compare(unit_str, "Hz"))
    factor = 1.0;
  else
    return std::nullopt;

  double value;
  const auto result{fast_float::from_chars(
      value_str.data(), value_str.data() + value_str.size(), value)};

  if (result.ec == std::errc::result_out_of_range)
    return std::nullopt;

  if (result.ec != std::errc{})
    return std::nullopt;

  return value * factor;
}

static std::string_view expect_line(TextCursor &cursor) {
  auto cur_line{cursor.read_line()};
  if (!cur_line.has_value())
    throw ParseError("Unexpected end of file");

  return *cur_line;
}

SweList Swe::parse_swe_file(TextCursor &cursor) {
  SweList result;
  // Loop over all the frequencies in the file
  while (true) {
    std::optional<std::string_view> cur_line;
    cur_line = cursor.read_line();
    // We are at the end of the file: no more frequencies
    if (!cur_line.has_value())
      break;

    // Try to parse the frequency, if it is present
    Swe cur_swe;
    cur_swe._frequency_hz = parse_frequency(*cur_line);

    // Skip one line of the header
    (void)expect_line(cursor);

    // This line contains NTHETA, NPHI, NMAX, MMAX
    cur_line = expect_line(cursor);
    auto [ntheta, nphi, nmax,
          mmax]{parse_numbers<int, int, int, int>(*cur_line)};
    cur_swe._n_theta = ntheta;
    cur_swe._n_phi = nphi;
    cur_swe._n_max = nmax;
    cur_swe._m_max = mmax;

    // Skip 5 lines
    for (int i{}; i < 5; ++i) {
      (void)expect_line(cursor);
    }

    cur_swe._coefficients.resize(cur_swe.num_of_coefficients());

    // Read the coefficients
    cur_swe._cum_power_w = 0.0;
    std::vector<Coefficient> cur_coefficients;
    for (size_t cur_abs_m{}; cur_abs_m <= cur_swe._m_max; ++cur_abs_m) {
      auto cur_coeff_line{expect_line(cursor)};

      auto [cur_abs_m_from_header,
            cur_power_w]{parse_numbers<size_t, double>(cur_coeff_line)};
      if (cur_abs_m != cur_abs_m_from_header) {
        throw ParseError(
            std::format("Unexpected value for |m|={} instead of {}",
                        cur_abs_m_from_header, cur_abs_m));
      }

      cur_swe._cum_power_w += cur_power_w;
      size_t n_start =
          std::max(static_cast<size_t>(1), static_cast<size_t>(cur_abs_m));

      if (cur_abs_m == 0) {
        cur_coefficients.resize(2 * cur_swe._n_max);
      } else {
        cur_coefficients.resize(4 * (cur_swe._n_max - (cur_abs_m - 1)));
      }

      for (size_t line_num{}; line_num < cur_coefficients.size() / 2;
           ++line_num)
        cursor.read_numeric_line(
            std::span{cur_coefficients.begin() + 2 * line_num,
                      cur_coefficients.begin() + 2 * (line_num + 1)});

      size_t coeff_idx{};
      for (size_t n{n_start}; n <= cur_swe._n_max; ++n) {
        if (cur_abs_m == 0) {
          cur_swe._coefficients.at(cur_swe.index(1, 0, n)) =
              cur_coefficients.at(coeff_idx++);
          cur_swe._coefficients.at(cur_swe.index(2, 0, n)) =
              cur_coefficients.at(coeff_idx++);
        } else {
          cur_swe._coefficients.at(cur_swe.index(1, -cur_abs_m, n)) =
              cur_coefficients.at(coeff_idx++);
          cur_swe._coefficients.at(cur_swe.index(2, -cur_abs_m, n)) =
              cur_coefficients.at(coeff_idx++);
          cur_swe._coefficients.at(cur_swe.index(1, +cur_abs_m, n)) =
              cur_coefficients.at(coeff_idx++);
          cur_swe._coefficients.at(cur_swe.index(2, +cur_abs_m, n)) =
              cur_coefficients.at(coeff_idx++);
        }
      }
    }

    result.emplace_back(cur_swe);
  }

  return result;
}
