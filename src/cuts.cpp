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

#include "cuts.hpp"
#include "fast_float/fast_float.h"
#include "parse_numbers.hpp"
#include "text_cursor.hpp"

#include <exception>
#include <format>

void Cut::parse_cut_file(TextCursor &cursor) {
  // The first line only contains text that can be discarded
  (void)cursor.read_line();

  const auto header_line{cursor.read_line()};
  if (!header_line.has_value())
    throw ParseError("Unexpected end of file while reading the cut header");

  auto [v_ini, v_inc, v_num, constant, icomp, icut, ncomp]{
      parse_numbers<double, double, int, double, int, int, int>(*header_line)};

  switch (icut) {
  case 1:
    _mode = CutMode::FixedAzimuth;
    break;
  case 2:
    _mode = CutMode::VaryingAzimuth;
    break;
  default:
    throw ParseError(
        std::format("Invalid value {} for ICUT (expected 1 or 2) in line {}",
                    icut, cursor.line_number() - 1));
  }

  _init_value = v_ini;
  _increment = v_inc;
  _constant_angle = constant;
  _num_of_values_in_cut = static_cast<std::size_t>(v_num);
  _component_count = static_cast<std::size_t>(ncomp);

  _coefficients.resize(_num_of_values_in_cut * _component_count);
  std::span<std::complex<double>> coefficients{_coefficients};

  try {
    for (std::size_t i{}; i < _num_of_values_in_cut; ++i) {
      cursor.read_numeric_line(
          coefficients.subspan(i * _component_count, _component_count));
    }
  } catch (const std::runtime_error &err) {
    // Convert any std::runtime_error raised by `TextCursor::read_numeric_line`
    // into a proper `ParserError`, including the current line number
    throw ParseError(
        std::format("Error at line {}: {}", cursor.line_number(), err.what()));
  }
}
