# -*- coding: utf-8 -*-

import sys
from random import uniform

from PySide2 import QtWidgets
from PySide2.QtTest import QTest

from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotMag import LamSlotMag
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSCIM import MachineSCIM
from pyleecan.Classes.MachineSIPMSM import MachineSIPMSM
from pyleecan.Classes.VentilationCirc import VentilationCirc
from pyleecan.Classes.VentilationTrap import VentilationTrap
from pyleecan.Classes.Material import Material
from pyleecan.GUI.Dialog.DMatLib.MatLib import MatLib
from pyleecan.GUI.Dialog.DMachineSetup.SLamParam.SLamParam import SLamParam


import pytest


@pytest.mark.GUI
class TestSLamParam(object):
    """Test that the widget SLamParam behave like it should"""

    def setup_method(self, method):
        """Run at the begining of every test to setup the gui"""
        self.test_obj = MachineSCIM()
        self.test_obj.stator = LamSlotWind(
            is_stator=True, L1=0.11, Kf1=0.12, Nrvd=12, Wrvd=0.13
        )
        self.test_obj.stator.mat_type.name = "test3"
        self.test_obj.rotor = LamSlotWind(
            is_stator=False, L1=0.21, Kf1=0.22, Nrvd=22, Wrvd=0.23
        )
        self.test_obj.rotor.mat_type.name = "test2"

        self.matlib = MatLib()
        self.matlib.dict_mat["RefMatLib"] = [
            Material(name="test1"),
            Material(name="test2"),
            Material(name="test3"),
        ]
        self.matlib.dict_mat["RefMatLib"][0].elec.rho = 0.31
        self.matlib.dict_mat["RefMatLib"][1].elec.rho = 0.32
        self.matlib.dict_mat["RefMatLib"][2].elec.rho = 0.33

        self.widget_1 = SLamParam(
            machine=self.test_obj, matlib=self.matlib, is_stator=True
        )
        self.widget_2 = SLamParam(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )

    @classmethod
    def setup_class(cls):
        """Start the app for the test"""
        print("\nStart Test SLamParam")
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

    @classmethod
    def teardown_class(cls):
        """Exit the app after the test"""
        cls.app.quit()

    def test_init(self):
        """Check that the Widget spinbox initialise to the lamination value"""

        assert self.widget_1.lf_L1.value() == 0.11
        assert self.widget_1.lf_Kf1.value() == 0.12
        assert self.widget_1.lf_Wrvd.value() == 0.13
        assert self.widget_1.si_Nrvd.value() == 12
        assert self.widget_1.w_mat.c_mat_type.currentIndex() == 2

        assert self.widget_2.lf_L1.value() == 0.21
        assert self.widget_2.lf_Kf1.value() == 0.22
        assert self.widget_2.lf_Wrvd.value() == 0.23
        assert self.widget_2.si_Nrvd.value() == 22
        assert self.widget_2.w_mat.c_mat_type.currentIndex() == 1

    def test_set_L1(self):
        """Check that the Widget allow to update L1"""
        # Clear the field before writing the new value
        self.widget_1.lf_L1.clear()
        value_1 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_1.lf_L1, str(value_1))
        self.widget_1.lf_L1.editingFinished.emit()  # To trigger the slot

        # Clear the field before writing the new value
        self.widget_2.lf_L1.clear()
        value_2 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_2.lf_L1, str(value_2))
        self.widget_2.lf_L1.editingFinished.emit()  # To trigger the slot

        assert self.test_obj.stator.L1 == value_1
        assert self.test_obj.rotor.L1 == value_2

    def test_set_Kf1(self):
        """Check that the Widget allow to update Kf1"""
        # Clear the field before writing the new value
        self.widget_1.lf_Kf1.clear()
        value_1 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_1.lf_Kf1, str(value_1))
        self.widget_1.lf_Kf1.editingFinished.emit()  # To trigger the slot

        # Clear the field before writing the new value
        self.widget_2.lf_Kf1.clear()
        value_2 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_2.lf_Kf1, str(value_2))
        self.widget_2.lf_Kf1.editingFinished.emit()  # To trigger the slot

        assert self.test_obj.stator.Kf1 == value_1
        assert self.test_obj.rotor.Kf1 == value_2

    def test_set_Wrvd(self):
        """Check that the Widget allow to update Wrvd"""
        # Clear the field before writing the new value
        self.widget_1.lf_Wrvd.clear()
        value_1 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_1.lf_Wrvd, str(value_1))
        self.widget_1.lf_Wrvd.editingFinished.emit()  # To trigger the slot

        # Clear the field before writing the new value
        self.widget_2.lf_Wrvd.clear()
        value_2 = round(uniform(0, 1), 4)
        QTest.keyClicks(self.widget_2.lf_Wrvd, str(value_2))
        self.widget_2.lf_Wrvd.editingFinished.emit()  # To trigger the slot

        assert self.test_obj.stator.Wrvd == value_1
        assert self.test_obj.rotor.Wrvd == value_2

    def test_set_Nrvd(self):
        """Check that the Widget allow to update Nrvd"""
        # Clear the field before writing the new value
        self.widget_1.si_Nrvd.clear()
        value_1 = int(uniform(1, 10))
        QTest.keyClicks(self.widget_1.si_Nrvd, str(value_1))
        self.widget_1.si_Nrvd.editingFinished.emit()  # To trigger the slot

        # Clear the field before writing the new value
        self.widget_2.si_Nrvd.clear()
        value_2 = int(uniform(1, 10))
        QTest.keyClicks(self.widget_2.si_Nrvd, str(value_2))
        self.widget_2.si_Nrvd.editingFinished.emit()  # To trigger the slot

        assert self.test_obj.stator.Nrvd == value_1
        assert self.test_obj.rotor.Nrvd == value_2

    def test_set_material(self):
        """Check that the combobox update the material"""
        self.widget_1.w_mat.c_mat_type.setCurrentIndex(0)
        assert self.test_obj.stator.mat_type.name == "test1"
        assert self.test_obj.stator.mat_type.elec.rho == 0.31

        self.widget_2.w_mat.c_mat_type.setCurrentIndex(2)
        assert self.test_obj.rotor.mat_type.name == "test3"
        assert self.test_obj.rotor.mat_type.elec.rho == 0.33

    def test_clean_vent(self):
        """Test that you can clean the ventilation"""

        assert not self.widget_1.g_ax_vent.isChecked()

        self.test_obj.stator.axial_vent = list()
        self.test_obj.stator.axial_vent.append(VentilationCirc(Zh=8))
        self.test_obj.stator.axial_vent.append(VentilationCirc(Zh=10))
        self.widget_1 = SLamParam(
            machine=self.test_obj, matlib=self.matlib, is_stator=True
        )
        assert self.widget_1.g_ax_vent.isChecked()

        self.widget_1.g_ax_vent.setChecked(False)
        assert self.test_obj.stator.axial_vent == list()

    def test_text_vent(self):
        """Test the text avd"""
        assert self.widget_1.out_axial_duct.text() == "Axial: 0 set (0 ducts)"

        self.test_obj.stator.axial_vent = list()
        self.test_obj.stator.axial_vent.append(VentilationCirc(Zh=8))
        self.test_obj.stator.axial_vent.append(VentilationCirc(Zh=10))
        self.widget_1 = SLamParam(
            machine=self.test_obj, matlib=self.matlib, is_stator=True
        )
        assert self.widget_1.out_axial_duct.text() == "Axial: 2 set (18 ducts)"

        self.test_obj.stator.axial_vent = list()
        self.test_obj.stator.axial_vent.append(VentilationTrap(Zh=20))
        self.widget_1 = SLamParam(
            machine=self.test_obj, matlib=self.matlib, is_stator=True
        )
        assert self.widget_1.out_axial_duct.text() == "Axial: 1 set (20 ducts)"
