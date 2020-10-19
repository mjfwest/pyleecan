# -*- coding: utf-8 -*-

import pytest

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.SurfLine import SurfLine
from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc3 import Arc3
from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.HoleM54 import HoleM54
from pyleecan.Methods.Slot.Hole.comp_surface import comp_surface
from numpy import exp, arcsin, ndarray, pi

# For AlmostEqual
DELTA = 1e-6

HoleM54_test = list()

test_obj = LamHole(is_internal=True, is_stator=False, hole=list(), Rext=0.1)
test_obj.hole = list()
test_obj.hole.append(HoleM54(Zh=8, W0=pi / 8, H0=30e-3, H1=10e-3, R1=60e-3))
HoleM54_test.append(
    {"test_obj": test_obj, "S_exp": 3.337942194e-4, "Rmin": 0.06, "Rmax": 0.0724515}
)


@pytest.mark.METHODS
class Test_HoleM54_meth(object):
    """pytest for HoleM54 methods"""

    @pytest.mark.parametrize("test_dict", HoleM54_test)
    def test_comp_surface(self, test_dict):
        """Check that the computation of the surface is correct"""
        test_obj = test_dict["test_obj"]
        result = test_obj.hole[0].comp_surface()

        a = result
        b = test_dict["S_exp"]
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < DELTA, msg

        # Check that the analytical method returns the same result as the numerical one
        b = comp_surface(test_obj.hole[0])
        msg = "Return " + str(a) + " expected " + str(b)
        assert abs((a - b) / a - 0) < 1e-4, msg

    @pytest.mark.parametrize("test_dict", HoleM54_test)
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

    @pytest.mark.parametrize("test_dict", HoleM54_test)
    def test_build_geometry(self, test_dict):
        """Check that the surf list is correct"""
        test_obj = LamHole(init_dict=test_dict["test_obj"].as_dict())
        result = test_obj.hole[0].build_geometry()
        assert len(result) == 1
        for surf in result:
            assert type(surf) == SurfLine

        assert result[0].label[:4] == "Hole"
        assert result[0].label[-9:] == "_R0_T0_S0"
        assert len(result[0].line_list) == 4
        assert type(result[0].line_list[0]) == Arc1
        assert type(result[0].line_list[1]) == Arc3
        assert type(result[0].line_list[2]) == Arc1
        assert type(result[0].line_list[3]) == Arc3
