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
#include <complex>
#include <optional>
#include <string_view>

#include "text_cursor.hpp"

std::optional<std::string_view> TextCursor::read_line() {
  if (_position == _contents.size()) {
    // We are at the end of the contents
    return std::nullopt;
  }

  const auto start = _position;
  const auto newline = _contents.find('\n', start);

  std::string_view line;

  if (newline == std::string_view::npos) {
    // No more line-ending character before the end of the contents
    line = _contents.substr(start);
    _position = _contents.size();
  } else {
    line = _contents.substr(start, newline - start);
    _position = newline + 1;
  }

  // This lets the parser to accept CR/LF without messing too much
  // with the rest of the code
  if (!line.empty() && line.back() == '\r') {
    line.remove_suffix(1);
  }

  ++_line_number;
  return line;
}

static void parse_numeric_line(std::string_view line,
                               std::span<std::complex<double>> output) {
  auto skip_spaces = [&] {
    while (!line.empty() && line.front() == ' ')
      line.remove_prefix(1);
  };

  auto read_double = [&]() -> double {
    skip_spaces();

    if (line.empty())
      throw std::runtime_error("Missing coefficient");

    const char *begin{line.data()};
    const char *end{begin + line.size()};

    double value;
    const auto result{fast_float::from_chars(begin, end, value)};

    if (result.ec == std::errc::result_out_of_range)
      throw std::runtime_error("Coefficient value out of range");

    if (result.ec != std::errc{})
      throw std::runtime_error("Invalid coefficient value");

    if (result.ptr != end && *result.ptr != ' ')
      throw std::runtime_error("Expected a space after coefficient value");

    line.remove_prefix(result.ptr - begin);
    return value;
  };

  for (auto &coefficient : output) {
    const double real{read_double()};
    const double imaginary{read_double()};

    coefficient = std::complex<double>{real, imaginary};
  }

  skip_spaces();

  if (!line.empty())
    throw std::runtime_error("Extra content after coefficients");
}

void TextCursor::read_numeric_line(std::span<std::complex<double>> output) {
  auto cur_line_opt{read_line()};

  if (!cur_line_opt.has_value())
    throw std::runtime_error("Unexpected empty content at line {}");

  parse_numeric_line(*cur_line_opt, output);
}
