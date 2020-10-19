# -*- coding: utf-8 -*-

import pytest

from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.SlotMFlat import SlotMFlat
from pyleecan.Classes.MagnetType13 import MagnetType13
from numpy import pi, exp, sqrt

Mag13_test = list()
# Internal Slot inset
lam = LamSlotMag(Rint=40e-3, Rext=90e-3, is_internal=True)
lam.slot = SlotMFlat(Zs=8, W0=0.04, H0=0.02, W3=2 * pi / 64)
lam.slot.magnet = [MagnetType13(Lmag=0.5, Hmag=0.02, Wmag=0.04, Rtop=0.04)]
Mag13_test.append({"test_obj": lam, "S_exp": 9.449e-4, "Ao": 0.5741029, "H_exp": 0.02})

# external slot inset
lam = LamSlotMag(Rint=110e-3, Rext=200e-3, is_internal=False)
lam.slot = SlotMFlat(Zs=4, W0=0.04, H0=0.025, W3=2 * pi / 64)
lam.slot.magnet = [MagnetType13(Lmag=0.5, Hmag=0.02, Wmag=0.04, Rtop=0.04)]
Mag13_test.append({"test_obj": lam, "S_exp": 9.44937e-4, "Ao": 0.298147, "H_exp": 0.02})

# Internal slot surface
lam = LamSlotMag(Rint=40e-3, Rext=90e-3, is_internal=True)
lam.slot = SlotMFlat(Zs=4, W0=0.08, H0=0)
lam.slot.magnet = [MagnetType13(Lmag=0.5, Hmag=0.02, Wmag=0.08, Rtop=0.0601)]
Mag13_test.append({"test_obj": lam, "S_exp": 2.43619e-3, "Ao": 0.9211, "H_exp": 0.02})

# For AlmostEqual
DELTA = 1e-4


@pytest.mark.METHODS
class Test_Magnet_Type_13_meth(object):
    """unittest for MagnetType13 methods"""

    @pytest.mark.parametrize("test_dict", Mag13_test)
    def test_comp_surface(self, test_dict):
        """Check that the computation of the surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.slot.magnet[0].comp_surface()

        a = result
        b = test_dict["S_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", Mag13_test)
    def test_comp_height(self, test_dict):
        """Check that the computation of the height is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.slot.magnet[0].comp_height()

        a = result
        b = test_dict["H_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", Mag13_test)
    def test_comp_angle_op(self, test_dict):
        """Check that the computation of the opening angle is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.slot.magnet[0].comp_angle_opening()

        a = result
        b = test_dict["Ao"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg
