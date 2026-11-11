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

  /* Conceptually, `_coefficients` is a 3D tensor with shape
   *
   *     (2, nmax, 2 * mmax + 1)
   *
   * but we model it as a 1D vector, where the fastest rank is the
   * latest (rightmost).
   */
  std::vector<Coefficient> _coefficients;

  [[nodiscard]]
  size_t index(int s, int m, int n) const noexcept {
    assert(n >= 1);
    assert(n <= static_cast<int>(_n_max));
    assert(abs(m) <= n);
    assert(abs(m) <= _m_max);

    /* To understand the (apparently) weird formula, remember that the
     * shape of `_coefficients` is (2, nmax, 2 * mmax + 1).
     *
     * Assume first that s=1 and n=1; then the first two terms in the
     * polynomial are null and the formula is simply a linear
     * operation on m:
     *
     *     index = m + mmax
     *
     * which, as m ∈ [-mmax, mmax], gives a number in the range
     *
     *     0 ≤ index ≤ 2 * mmax
     *
     * Suppose now to increment `n` by one, so that n=2. In this case,
     * we have moved to the next row, which means that the first row
     * was already “filled”. The formula becomes
     *
     *     index = (2 * mmax + 1) + (m + mmax)
     *
     * where the first term skips the elements of the first row and
     * the second term applies to the second row only. Iterate this
     * for all the other values of n and nearly all the formula makes
     * sense! The `s` term can be analyzed in a similar way, but
     * instead of “filling” one row at a time, we are filling a
     * rectangle, hence the multiplication of two dimensions.
     */
    size_t dim1{2 * _m_max + 1};
    size_t dim2{_n_max};
    return (s - 1) * (dim1 * dim2) + dim1 * (n - 1) + (m + _m_max);
  }

  static std::optional<double> parse_frequency(std::string_view line);
};

#endif
