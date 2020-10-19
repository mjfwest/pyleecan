# -*- coding: utf-8 -*-
from os import chdir

chdir("../../..")

from os.path import join

from numpy import (
    array,
    linspace,
    ones,
    pi,
    sqrt,
    cos,
    transpose,
    zeros,
    abs as np_abs,
    angle as np_angle,
)
from numpy.testing import assert_array_almost_equal
import matplotlib.pyplot as plt
from pyleecan.Classes.ImportGenMatrixSin import ImportGenMatrixSin
from pyleecan.Classes.ImportGenVectLin import ImportGenVectLin
from pyleecan.Classes.ImportGenVectSin import ImportGenVectSin
from pyleecan.Classes.ImportMatrixVal import ImportMatrixVal
from pyleecan.Classes.InputCurrent import InputCurrent
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.MachineDFIM import MachineDFIM
from pyleecan.Classes.Output import Output
from pyleecan.Classes.Simulation import Simulation
from pyleecan.definitions import DATA_DIR
from pyleecan.Functions.load import load
from pyleecan.Methods.Simulation.Input import InputError
import pytest
from Tests import save_plot_path as save_path

IPMSM_A = load(join(DATA_DIR, "Machine", "IPMSM_A.json"))
InputCurrent_Error_test = list()
time_wrong = ImportMatrixVal(value=zeros((10, 2)))
time = ImportGenVectLin(0, 10, 100)

angle_wrong = ImportMatrixVal(value=zeros((10, 4)))
angle = ImportGenVectLin(0, 2 * pi, 1024)

I_1 = ImportMatrixVal(value=zeros((100, 3)))
I_2 = ImportMatrixVal(value=zeros((100, 2)))
I_3 = ImportMatrixVal(value=zeros((2, 100)))
I_4 = ImportMatrixVal(value=zeros((100)))

angle_rotor_wrong = ImportMatrixVal(value=zeros((10, 2)))
angle_rotor_wrong2 = ImportMatrixVal(value=zeros((102)))
angle_rotor = ImportMatrixVal(value=zeros((100)))

# Quick fix added by Cedric 30/07/20 Nr -> N0
N0_wrong = 1
N0_wrong2 = 1
N0 = 1

# Winding stator only
M1 = MachineDFIM()
M1.stator = LamSlotWind()
M1.stator.winding.qs = 3
M1.rotor.winding = None
# Winding rotor only
M2 = MachineDFIM()
M2.rotor = LamSlotWind()
M2.rotor.winding.qs = 2
M2.stator.winding = None
# Winding rotor + stator
M3 = MachineDFIM()
M3.stator = LamSlotWind()
M3.stator.winding.qs = 3
M3.rotor = LamSlotWind()
M3.rotor.winding.qs = 2


# Wrong time
test_obj = Simulation(machine=IPMSM_A)
test_obj.input = InputCurrent(time=None)
InputCurrent_Error_test.append(
    {"test_obj": test_obj, "exp": "ERROR: InputCurrent.time missing"}
)
# Wong time shape
test_obj = Simulation(machine=IPMSM_A)
test_obj.input = InputCurrent(time=time_wrong)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.time should be a vector, (10, 2) shape found",
    }
)
# Wrong angle shape
test_obj = Simulation(machine=IPMSM_A)
test_obj.input = InputCurrent(time=time, angle=angle_wrong)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.angle should be a vector, (10, 4) shape found",
    }
)
# Missing Is
test_obj = Simulation(machine=M1)
test_obj.input = InputCurrent(time=time, angle=angle, Is=None)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.Is, InputCurrent.Id_ref, and InputCurrent.Iq_ref missing",
    }
)
# Is wrong shape
test_obj = Simulation(machine=M1)
test_obj.input = InputCurrent(time=time, angle=angle, Is=I_3)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.Is must be a matrix with the shape (100, 3) (len(time), stator phase number), (2, 100) returned",
    }
)
test_obj = Simulation(machine=M1)
test_obj.input = InputCurrent(time=time, angle=angle, Is=I_4)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.Is must be a matrix with the shape (100, 3) (len(time), stator phase number), (100,) returned",
    }
)
# Wrong Ir
test_obj = Simulation(machine=M2)
test_obj.input = InputCurrent(time=time, angle=angle, Ir=None)
InputCurrent_Error_test.append(
    {"test_obj": test_obj, "exp": "ERROR: InputCurrent.Ir missing"}
)
test_obj = Simulation(machine=M2)
test_obj.input = InputCurrent(time=time, angle=angle, Ir=I_3)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.Ir must be a matrix with the shape (100, 2) (len(time), rotor phase number), (2, 100) returned",
    }
)
test_obj = Simulation(machine=M2)
test_obj.input = InputCurrent(time=time, angle=angle, Ir=I_4)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.Ir must be a matrix with the shape (100, 2) (len(time), rotor phase number), (100,) returned",
    }
)
# Wrong N0, alpha_rotor
test_obj = Simulation(machine=M3)
test_obj.input = InputCurrent(
    time=time, angle=angle, Is=I_1, Ir=I_2, angle_rotor=None, N0=None
)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.angle_rotor and InputCurrent.N0 can't be None at the same time",
    }
)
test_obj = Simulation(machine=M3)
test_obj.input = InputCurrent(
    time=time, angle=angle, Is=I_1, Ir=I_2, angle_rotor=angle_rotor_wrong, N0=None
)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.angle_rotor should be a vector of the same length as time, (10, 2) shape found, (100,) expected",
    }
)
test_obj = Simulation(machine=M3)
test_obj.input = InputCurrent(
    time=time, angle=angle, Is=I_1, Ir=I_2, angle_rotor=angle_rotor_wrong2, N0=None
)
InputCurrent_Error_test.append(
    {
        "test_obj": test_obj,
        "exp": "ERROR: InputCurrent.angle_rotor should be a vector of the same length as time, (102,) shape found, (100,) expected",
    }
)

idq_test = list()
idq_test.append({"Id": 2, "Iq": 0})
idq_test.append({"Id": 0, "Iq": 2})
idq_test.append({"Id": sqrt(2), "Iq": sqrt(2)})


@pytest.mark.METHODS
class Test_InCurrent_meth(object):
    """unittest for InputCurrent object methods"""

    @pytest.mark.parametrize("test_dict", InputCurrent_Error_test)
    def test_InputCurrent_Error_test(self, test_dict):
        """Check that the input current raises the correct errors"""
        output = Output(simu=test_dict["test_obj"])
        with pytest.raises(InputError) as context:
            output.simu.input.gen_input()
            assert test_dict["exp"] == str(context.exception)

    @pytest.mark.parametrize("test_dict", idq_test)
    def test_InputCurrent_DQ(self, test_dict):
        """Enforce Id/Iq, check Is then enforce Is, check Id/Iq"""
        test_obj = Simulation(machine=IPMSM_A)
        output = Output(simu=test_obj)
        Nt_tot = 70
        Na_tot = 20
        N0 = 2000

        # In RMS cf .csv conventions
        Id_ref = test_dict["Id"]
        Iq_ref = test_dict["Iq"]

        # Compute expected current
        A_rms = np_abs(Id_ref + 1j * Iq_ref)
        Phi0 = np_angle(Id_ref + 1j * Iq_ref)
        qs = IPMSM_A.stator.winding.qs
        p = IPMSM_A.stator.get_pole_pair_number()
        time_exp = linspace(0, 60 / N0, Nt_tot, endpoint=False)
        felec = p * N0 / 60
        rot_dir = IPMSM_A.stator.comp_rot_dir()
        Ia = (
            A_rms
            * sqrt(2)
            * cos(2 * pi * felec * time_exp + 0 * rot_dir * 2 * pi / qs + Phi0)
        )
        Ib = (
            A_rms
            * sqrt(2)
            * cos(2 * pi * felec * time_exp + 1 * rot_dir * 2 * pi / qs + Phi0)
        )
        Ic = (
            A_rms
            * sqrt(2)
            * cos(2 * pi * felec * time_exp + 2 * rot_dir * 2 * pi / qs + Phi0)
        )
        Is_exp = array([Ia, Ib, Ic])

        # Compute expected rotor position
        angle_rotor_initial = IPMSM_A.comp_angle_offset_initial()
        # rot_dir is the rotation direction of the fundamental magnetic field
        # Then rotor position is -1 * rot_dir
        angle_rotor_exp = (
            linspace(0, -1 * rot_dir * 2 * pi, Nt_tot, endpoint=False)
            + angle_rotor_initial
        )

        test_obj.input = InputCurrent(
            Nt_tot=Nt_tot,
            Na_tot=Na_tot,
            Is=None,
            Iq_ref=Iq_ref,
            Id_ref=Id_ref,
            Ir=None,
            angle_rotor=None,  # Will be computed according to N0 and rot_dir
            N0=N0,
            rot_dir=None,
        )

        # Generate Is according to Id/Iq
        test_obj.input.gen_input()
        assert_array_almost_equal(
            output.elec.time.get_values(is_oneperiod=False),
            time_exp,
        )
        assert_array_almost_equal(
            output.elec.angle.get_values(is_oneperiod=False),
            linspace(0, 2 * pi, Na_tot, endpoint=False),
        )
        assert_array_almost_equal(output.elec.get_Is().values, Is_exp)
        assert_array_almost_equal(output.get_angle_rotor(), angle_rotor_exp)
        assert_array_almost_equal(output.elec.N0, N0)
        assert_array_almost_equal(output.geo.rot_dir, rot_dir)

        # Check Id/Iq by enforcing Is
        test_obj.input = InputCurrent(
            Nt_tot=Nt_tot,
            Na_tot=Na_tot,
            Is=Is_exp.transpose(),
            Iq_ref=None,
            Id_ref=None,
            Ir=None,
            angle_rotor=None,  # Will be computed according to N0 and rot_dir
            N0=N0,
            rot_dir=None,
        )
        out = Output(simu=test_obj)
        test_obj.input.gen_input()
        assert out.elec.Id_ref == pytest.approx(test_dict["Id"], abs=0.01)
        assert out.elec.Iq_ref == pytest.approx(test_dict["Iq"], abs=0.01)

        out.plot_A_time("elec.Is", index_list=[0, 1, 2])
        title = "Id=" + str(test_dict["Id"]) + " Iq=" + str(test_dict["Iq"])
        fig = plt.gcf()
        plt.title(title)
        fig.savefig(
            join(
                save_path,
                "test_InCurrent_Id="
                + str(test_dict["Id"])
                + "_Iq="
                + str(test_dict["Iq"])
                + ".png",
            )
        )
        plt.close("all")
