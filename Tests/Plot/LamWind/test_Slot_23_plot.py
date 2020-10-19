# -*- coding: utf-8 -*-
from os.path import join

import matplotlib.pyplot as plt
from numpy import array, pi, zeros

from pyleecan.Classes.Frame import Frame
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.LamSquirrelCage import LamSquirrelCage
from pyleecan.Classes.MachineDFIM import MachineDFIM
from pyleecan.Classes.Shaft import Shaft
from pyleecan.Classes.VentilationCirc import VentilationCirc
from pyleecan.Classes.VentilationPolar import VentilationPolar
from pyleecan.Classes.VentilationTrap import VentilationTrap
from pyleecan.Classes.Winding import Winding
from pyleecan.Classes.WindingUD import WindingUD
from pyleecan.Classes.WindingCW2LT import WindingCW2LT
from pyleecan.Classes.WindingDW2L import WindingDW2L
from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.Classes.SlotW23 import SlotW23

from Tests import save_plot_path as save_path
from Tests.Plot.LamWind import wind_mat

import pytest

"""pytest for Lamination with winding plot"""


@pytest.mark.PLOT
class Test_Slot_23_plot(object):
    def test_Lam_Wind_23_wind_22(self):
        """Test machine plot with Slot 23 and winding rad=2, tan=2"""
        print("\nTest plot Slot 23")
        plt.close("all")
        test_obj = MachineDFIM()
        test_obj.rotor = LamSlotWind(
            Rint=0,
            Rext=0.5,
            is_internal=True,
            is_stator=False,
            L1=0.9,
            Nrvd=5,
            Wrvd=0.02,
        )
        test_obj.rotor.slot = SlotW23(
            Zs=6, W0=50e-3, W1=90e-3, W2=100e-3, H0=20e-3, H1=35e-3, H2=130e-3
        )
        test_obj.rotor.winding = WindingUD(
            user_wind_mat=wind_mat, qs=4, p=4, Lewout=60e-3
        )
        test_obj.rotor.mat_type.mag = MatMagnetics(Wlam=0.5e-3)
        test_obj.shaft = Shaft(Drsh=test_obj.rotor.Rint * 2, Lshaft=1)

        test_obj.stator = LamSlotWind(
            Rint=0.51,
            Rext=0.8,
            is_internal=False,
            is_stator=True,
            L1=0.9,
            Nrvd=5,
            Wrvd=0.02,
        )
        test_obj.stator.slot = SlotW23(
            Zs=18, W0=50e-3, W1=80e-3, W2=50e-3, H0=15e-3, H1=0, H2=170e-3
        )
        test_obj.stator.winding = WindingDW2L(qs=3, p=3)
        test_obj.stator.mat_type.mag = MatMagnetics(Wlam=0.5e-3)
        test_obj.stator.winding.Lewout = 60e-3
        test_obj.frame = Frame(Rint=0.8, Rext=1, Lfra=1)

        test_obj.plot()
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s23_1-Machine.png"))
        # Rotor + Stator + 2 for frame + 0 shaft
        assert len(fig.axes[0].patches) == 65

        test_obj.rotor.plot()
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s23_2-Rotor.png"))
        # 1 for lam + Zs*4 for wind
        assert len(fig.axes[0].patches) == 25

        test_obj.stator.plot()
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s23_3-Stator.png"))
        # 2 for lam + Zs *2 for wind
        assert len(fig.axes[0].patches) == 38

        tooth = test_obj.rotor.slot.get_surface_tooth()
        tooth.plot(color="r")
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s23_Tooth_in.png"))

        tooth = test_obj.stator.slot.get_surface_tooth()
        tooth.plot(color="r")
        fig = plt.gcf()
        fig.savefig(join(save_path, "test_Lam_Wind_s23_Tooth_out.png"))
