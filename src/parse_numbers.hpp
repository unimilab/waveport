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

#ifndef __PARSE_NUMBERS_HPP__
#define __PARSE_NUMBERS_HPP__

#include <format>
#include <stdexcept>
#include <string_view>
#include <system_error>
#include <tuple>

class ParseError : public std::runtime_error {
public:
  using std::runtime_error::runtime_error;
};

/// \brief Read a set of numbers from a text line
///
/// This template function reads a set of floating-point or integer
/// numbers from a line of text and returns them as a tuple. It throws
/// a \a ParseError exception if any error occurs while parsing the
/// line.
///
/// This function is handy when you know at compile time how many
/// numbers you have to read and their type. It is *not* suitable
/// when the number of elements in the line is determined at runtime:
/// in that case, use \ref TextCursor::parse_numeric_line.
///
/// \param line The line to parse
/// \return A tuple containing the parsed numbers
template <class... Ts>
[[nodiscard]] std::tuple<Ts...> parse_numbers(std::string_view line) {
  std::string_view remaining{line};
  std::size_t field{};

  auto fail = [&](std::string_view reason) {
    throw ParseError(std::format("Numeric field {}: {} in line \"{}\"", field,
                                 reason, line));
  };

  auto skip_spaces = [&] {
    while (!remaining.empty() && remaining.front() == ' ')
      remaining.remove_prefix(1);
  };

  auto read_number = [&](auto &value) {
    ++field;
    skip_spaces();

    if (remaining.empty())
      fail("missing value");

    const char *begin{remaining.data()};
    const char *end{begin + remaining.size()};
    const auto result{fast_float::from_chars(begin, end, value)};

    if (result.ec == std::errc::result_out_of_range)
      fail("value out of range");

    if (result.ec != std::errc{})
      fail("invalid number");

    if (result.ptr != end && *result.ptr != ' ')
      fail("expected a space after the number");

    remaining.remove_prefix(result.ptr - begin);
  };

  std::tuple<Ts...> values{};

  std::apply([&](auto &...value) { (read_number(value), ...); }, values);

  skip_spaces();

  if (!remaining.empty()) {
    ++field;
    fail("unexpected extra content at the end");
  }

  return values;
}

#endif
