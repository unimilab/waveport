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

#ifndef __TEXT_CURSOR_HPP__
#define __TEXT_CURSOR_HPP__

#include <complex>
#include <optional>
#include <span>
#include <string_view>

class TextCursor {
private:
  std::string_view _contents;
  std::size_t _position{};
  std::size_t _line_number{1};

public:
  explicit TextCursor(std::string_view contents) : _contents(contents) {}

  [[nodiscard]]
  std::optional<std::string_view> read_line();

  [[nodiscard]]
  bool at_end() const noexcept {
    return _position == _contents.size();
  }

  [[nodiscard]]
  std::size_t line_number() const noexcept {
    return _line_number;
  }

  [[nodiscard]]
  std::size_t byte_offset() const noexcept {
    return _position;
  }

  void read_numeric_line(std::span<std::complex<double>> output);
};

#endif
