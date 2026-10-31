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

#ifndef __COMPONENT_TYPE_HPP__
#define __COMPONENT_TYPE_HPP__

enum class ComponentType {
  LinearThetaPhi = 1,
  Circular = 2,
  CoCross = 3,
  LinearAlongPolEllipse = 4,
  XPDThetaPhi = 5,
  XPDCircular = 6,
  XPDCoCross = 7,
  XPDPolEllipse = 8,
  TotalPowerAndCircularRatio = 9,
  PoyntingVector = 11,
};

#endif
