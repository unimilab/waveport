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

#ifndef __SWE_HPP__
#define __SWE_HPP__

#include "component_type.hpp"
#include "text_cursor.hpp"

#include <cassert>
#include <complex>
#include <optional>
#include <string>
#include <string_view>
#include <vector>

class Swe;
using SweList = std::vector<Swe>;

class Swe {
public:
  using Coefficient = std::complex<double>;

  explicit Swe() {}

  [[nodiscard]]
  std::optional<double> frequency_hz() const noexcept {
    return _frequency_hz;
  }

  [[nodiscard]]
  const Coefficient *coefficients_data() const noexcept {
    return _coefficients.data();
  }

  [[nodiscard]]
  bool are_indexes_valid(int s, int m, int n) const noexcept {
    if (n < 1 || abs(m) > n || abs(m) > _m_max)
      return false;

    return true;
  }

  [[nodiscard]]
  Coefficient coefficient(int s, int m, int n) const noexcept {
    if (!are_indexes_valid(s, m, n))
      return std::complex<double>{0.0, 0.0};

    Coefficient result{_coefficients.at(index(s, m, n))};
    return result;
  }

  [[nodiscard]]
  size_t num_of_coefficients() const noexcept {
    /* See the comment in the implementation of `Swe::index` to
     * understand how coefficients are laid in memory within
     * `_coefficients`. */
    return 2 * (_n_max * (_n_max + 1) + _m_max);
  }

  [[nodiscard]] size_t num_of_theta() const noexcept { return _n_theta; }
  [[nodiscard]] size_t num_of_phi() const noexcept { return _n_phi; }
  [[nodiscard]] size_t n_max() const noexcept { return _n_max; }
  [[nodiscard]] size_t m_max() const noexcept { return _m_max; }

  [[nodiscard]]
  double cum_power_w() const noexcept {
    return _cum_power_w;
  }

  static SweList parse_swe_file(TextCursor &cursor);

private:
  std::optional<double> _frequency_hz;
  size_t _n_theta;
  size_t _n_phi;
  size_t _n_max;
  size_t _m_max;
  double _cum_power_w;

  /* See the comment in the implementation of `Swe::index` to
   * understand how coefficients are laid in memory within
   * `_coefficients`. */
  std::vector<Coefficient> _coefficients;

  [[nodiscard]]
  size_t index(int s, int m, int n) const noexcept {
    assert(n >= 1);
    assert(n <= static_cast<int>(_n_max));
    assert(abs(m) <= n);
    assert(abs(m) <= _m_max);

    /* The memory layout follows an idea explained in Hansen’s book and
     * illustrated in Fig. 2.3, which is reproduced here:
     *
     *      ^ m
     *      |                  j=30
     *    3 +                      o
     *      |                    29
     *      |
     *      |            16      28
     *    2 +              o       o
     *      |            15      27
     *      |
     *      |      6      14      26
     *    1 +       o       o       o
     *      |      5      13      25
     *      |
     *      |      4      12      24
     *    0 +-------o-------o-------o-------+--->
     *      |      3      11      23      n=4
     *      |
     *      |      2      10      22
     *   −1 +       o       o       o
     *      |    j=1       9      21
     *      |
     *      |             8      20
     *   −2 +              o       o
     *      |             7      19
     *      |
     *      |                    18
     *   −3 +                      o
     *      |                    17
     *
     * Each "o" point represents *two* coefficients: the one with s=1
     * and the one with s=2. The `j` index varies linearly from 1 to
     * 30 in the figure, touching all the coefficients.
     */

    // Hansen does not put the `- 1` at the end because he assumes
    // 1-based indexing (Fortran’s convention)
    return 2 * (n * (n + 1) + m - 1) + s - 1;
  }

  static std::optional<double> parse_frequency(std::string_view line);
};

#endif
