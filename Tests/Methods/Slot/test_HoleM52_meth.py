# -*- coding: utf-8 -*-

import pytest

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.SurfLine import SurfLine

from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.HoleM52 import HoleM52
from numpy import exp, arcsin, ndarray, pi

# For AlmostEqual
DELTA = 1e-6

HoleM52_test = list()

test_obj = LamHole(is_internal=True, is_stator=False, hole=list(), Rext=0.1)
test_obj.hole = list()
test_obj.hole.append(HoleM52(Zh=8, W0=30e-3, W3=15e-3, H0=12e-3, H1=18e-3, H2=2e-3))
HoleM52_test.append(
    {
        "test_obj": test_obj,
        "S_exp": 8.059458e-4,
        "SM_exp": 5.4e-4,
        "Rmin": 6.587571e-2,
        "Rmax": 8.8e-2,
        "W1": 4.9971e-3,
        "alpha": 0.614736,
    }
)


@pytest.mark.METHODS
class Test_Hole52_meth(object):
    """pytest for holeB52 methods"""

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_comp_surface(self, test_dict):
        """Check that the computation of the surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_surface()

        a = result
        b = test_dict["S_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_comp_surface_mag(self, test_dict):
        """Check that the computation of the magnet surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_surface_magnets()

        a = result
        b = test_dict["SM_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_comp_alpha(self, test_dict):
        """Check that the computation of the alpha is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_alpha()

        a = result
        b = test_dict["alpha"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_comp_W1(self, test_dict):
        """Check that the computation of W1 is correct"""
        test_obj = test_dict["test_obj"]

        a = test_obj.hole[0].comp_W1()
        b = test_dict["W1"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_comp_radius(self, test_dict):
        """Check that the computation of the radius is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_radius()

        a = result[0]
        b = test_dict["Rmin"]
        msg = "For Rmin: Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

        a = result[1]
        b = test_dict["Rmax"]
        msg = "For Rmax: Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_build_geometry_with_magnet(self, test_dict):
        """Check that the surf list is correct with magnet"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].build_geometry()
        assert len(result) == 3
        for surf in result:
            assert type(surf) == SurfLine

        assert result[0].label[:5] == "Hole_"
        assert result[0].label[-9:] == "_R0_T0_S0"
        assert len(result[0].line_list) == 4

        assert result[1].label[:11] == "HoleMagnet_"
        assert result[1].label[-11:] == "_N_R0_T0_S0"
        assert len(result[1].line_list) == 4

        assert result[2].label[:5] == "Hole_"
        assert result[2].label[-9:] == "_R0_T1_S0"
        assert len(result[2].line_list) == 4

    @pytest.mark.parametrize("test_dict", HoleM52_test)
    def test_build_geometry_no_magnet(self, test_dict):
        """Check that the surf list is correct without magnet"""
        test_obj = LamHole(init_dict=test_dict["test_obj"].as_dict())
        test_obj.hole[0].magnet_0 = None
        result = test_obj.hole[0].build_geometry()
        assert len(result) == 1
        for surf in result:
            assert type(surf) == SurfLine

        assert result[0].label[:5] == "Hole_"
        assert result[0].label[-9:] == "_R0_T0_S0"
        assert len(result[0].line_list) == 8
