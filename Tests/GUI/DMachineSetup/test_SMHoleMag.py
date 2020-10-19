# -*- coding: utf-8 -*-

import sys

from PySide2 import QtWidgets

from pyleecan.Classes.LamHole import LamHole
from pyleecan.Classes.LamSlotWind import LamSlotWind
from pyleecan.Classes.MachineIPMSM import MachineIPMSM
from pyleecan.Classes.MachineSyRM import MachineSyRM
from pyleecan.Classes.Magnet import Magnet
from pyleecan.Classes.HoleM50 import HoleM50
from pyleecan.Classes.HoleM51 import HoleM51
from pyleecan.Classes.HoleM52 import HoleM52
from pyleecan.Classes.HoleM53 import HoleM53
from pyleecan.Classes.HoleM54 import HoleM54
from pyleecan.Classes.HoleM57 import HoleM57
from pyleecan.Classes.HoleM58 import HoleM58
from pyleecan.GUI.Dialog.DMatLib.MatLib import MatLib
from pyleecan.GUI.Dialog.DMachineSetup.SMHoleMag.SMHoleMag import SMHoleMag
from pyleecan.Classes.Material import Material


import pytest


@pytest.mark.GUI
class TestSMHoleMag(object):
    """Test that the widget SMHoleMag behave like it should"""

    def setup_method(self, method):
        """Run at the begining of every test to setup the gui"""

        self.test_obj = MachineIPMSM(type_machine=8)
        self.test_obj.stator = LamSlotWind()
        self.test_obj.stator.winding.p = 4
        self.test_obj.rotor = LamHole(Rint=0.1, Rext=0.2)
        self.test_obj.rotor.hole = list()
        self.test_obj.rotor.hole.append(HoleM50(Zh=8))
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet3"

        self.test_obj2 = MachineSyRM(type_machine=5)
        self.test_obj2.stator = LamSlotWind()
        self.test_obj2.stator.winding.p = 4
        self.test_obj2.rotor = LamHole(Rint=0.1, Rext=0.2)
        self.test_obj2.rotor.hole = list()
        self.test_obj2.rotor.hole.append(HoleM54(Zh=16))

        self.matlib = MatLib()
        self.matlib.list_mat = [
            Material(name="Magnet1"),
            Material(name="Magnet2"),
            Material(name="Magnet3"),
        ]
        self.matlib.index_first_mat_mach = 3

        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        self.widget2 = SMHoleMag(
            machine=self.test_obj2, matlib=self.matlib, is_stator=False
        )

    @classmethod
    def setup_class(cls):
        """Start the app for the test"""
        print("\nStart Test SWSlot")
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

    @classmethod
    def teardown_class(cls):
        """Exit the app after the test"""
        cls.app.quit()

    def test_init(self):
        """Check that the Widget initialize to the correct hole"""

        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.count() == 1
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 0
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 50"
        )
        assert self.widget.tab_hole.widget(0).c_hole_type.count() == 6

    def test_init_SyRM(self):
        """Check that the Widget initialize to the correct hole"""

        assert self.widget2.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 22.5 °"
        assert self.widget2.tab_hole.count() == 1
        assert self.widget2.tab_hole.widget(0).c_hole_type.currentIndex() == 4
        assert (
            self.widget2.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 54"
        )
        assert self.widget2.tab_hole.widget(0).c_hole_type.count() == 7

    def test_init_SyRM_51(self):
        """Check that the Widget initialize to the correct hole"""

        self.test_obj2.rotor.hole = list()
        self.test_obj2.rotor.hole.append(
            HoleM51(
                Zh=16,
                W0=0.11,
                W1=0.12,
                W2=0.13,
                W3=0.14,
                W4=0.15,
                W5=0.16,
                W6=0.17,
                W7=0.18,
                H0=0.19,
                H1=0.2,
                H2=0.21,
            )
        )
        self.test_obj2.rotor.hole[0].remove_magnet()
        self.widget2 = SMHoleMag(
            machine=self.test_obj2, matlib=self.matlib, is_stator=False
        )
        assert self.widget2.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 22.5 °"
        assert self.widget2.tab_hole.count() == 1
        assert self.widget2.tab_hole.widget(0).c_hole_type.currentIndex() == 1
        assert (
            self.widget2.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 51"
        )
        assert self.widget2.tab_hole.widget(0).c_hole_type.count() == 7

        assert self.widget2.tab_hole.widget(0).w_hole.lf_W0.text() == "0.11"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W1.text() == "0.12"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W2.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W3.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W4.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W5.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W6.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_W7.text() == "0"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_H0.text() == "0.19"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_H1.text() == "0.2"
        assert self.widget2.tab_hole.widget(0).w_hole.lf_H2.text() == "0.21"

    def test_init_51(self):
        """Check that you can edit a hole 51"""
        self.test_obj.rotor.hole[0] = HoleM51(Zh=18)
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet1"
        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 20 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 1
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 51"
        )

    def test_init_52(self):
        """Check that you can edit a hole 52"""
        self.test_obj.rotor.hole[0] = HoleM52(Zh=18)
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet1"
        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 20 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 2
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 52"
        )

    def test_init_53(self):
        """Check that you can edit a hole 53"""
        self.test_obj.rotor.hole[0] = HoleM53(Zh=11)
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet1"
        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 32.73 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 3
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 53"
        )

    def test_init_57(self):
        """Check that you can edit a hole 57"""
        self.test_obj.rotor.hole[0] = HoleM57(Zh=18)
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet1"
        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 20 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 4
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 57"
        )

    def test_init_58(self):
        """Check that you can edit a hole 58"""
        self.test_obj.rotor.hole[0] = HoleM58(Zh=18)
        self.test_obj.rotor.hole[0].magnet_0.mat_type.name = "Magnet1"
        self.widget = SMHoleMag(
            machine=self.test_obj, matlib=self.matlib, is_stator=False
        )
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 20 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 5
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 58"
        )

    def test_set_type_51(self):
        """ """
        self.widget.tab_hole.widget(0).c_hole_type.setCurrentIndex(1)

        assert type(self.test_obj.rotor.hole[0]) == HoleM51
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 1
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 51"
        )

    def test_set_type_52(self):
        """ """
        self.widget.tab_hole.widget(0).c_hole_type.setCurrentIndex(2)

        assert type(self.test_obj.rotor.hole[0]) == HoleM52
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 2
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 52"
        )

    def test_set_type_53(self):
        """ """
        self.widget.tab_hole.widget(0).c_hole_type.setCurrentIndex(3)

        assert type(self.test_obj.rotor.hole[0]) == HoleM53
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 3
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 53"
        )

    def test_set_type_57(self):
        """ """
        self.widget.tab_hole.widget(0).c_hole_type.setCurrentIndex(4)

        assert type(self.test_obj.rotor.hole[0]) == HoleM57
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 4
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 57"
        )

    def test_set_type_58(self):
        """ """
        self.widget.tab_hole.widget(0).c_hole_type.setCurrentIndex(5)

        assert type(self.test_obj.rotor.hole[0]) == HoleM58
        assert self.widget.out_hole_pitch.text() == "Slot pitch = 360 / 2p = 45 °"
        assert self.widget.tab_hole.widget(0).c_hole_type.currentIndex() == 5
        assert (
            self.widget.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 58"
        )

    def test_SyRM_set_type_54_51_54(self):
        """Set a type 54 for a SyRM then set a 51 to check how the magnets are handled"""
        # Init a HoleM54
        assert self.widget2.tab_hole.widget(0).c_hole_type.currentIndex() == 4
        assert (
            self.widget2.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 54"
        )
        assert self.test_obj2.rotor.hole[0].Zh == 16

        # Set type 51
        self.widget2.tab_hole.widget(0).c_hole_type.setCurrentIndex(1)
        assert self.widget2.tab_hole.widget(0).c_hole_type.currentIndex() == 1
        assert (
            self.widget2.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 51"
        )
        assert type(self.test_obj2.rotor.hole[0]) == HoleM51
        assert self.test_obj2.rotor.hole[0].magnet_0 == None
        assert self.test_obj2.rotor.hole[0].Zh == 16

        # Set type 54
        self.widget2.tab_hole.widget(0).c_hole_type.setCurrentIndex(4)
        assert self.widget2.tab_hole.widget(0).c_hole_type.currentIndex() == 4
        assert (
            self.widget2.tab_hole.widget(0).c_hole_type.currentText() == "Slot Type 54"
        )
        assert type(self.test_obj2.rotor.hole[0]) == HoleM54
        assert self.test_obj2.rotor.hole[0].Zh == 16

    def test_add_remove_hole(self):
        assert len(self.test_obj.rotor.hole) == 1
        assert self.widget.tab_hole.count() == 1

        self.widget.b_add.clicked.emit()

        assert len(self.test_obj.rotor.hole) == 2
        assert type(self.test_obj.rotor.hole[1]) == HoleM50
        assert self.test_obj.rotor.hole[1].Zh == 8
        assert self.widget.tab_hole.count() == 2

        self.widget.b_add.clicked.emit()

        assert len(self.test_obj.rotor.hole) == 3
        assert type(self.test_obj.rotor.hole[2]) == HoleM50
        assert self.test_obj.rotor.hole[2].Zh == 8
        assert self.widget.tab_hole.count() == 3
        assert self.widget.tab_hole.tabText(0) == "Slot 1"
        assert self.widget.tab_hole.tabText(1) == "Slot 2"
        assert self.widget.tab_hole.tabText(2) == "Slot 3"

        self.widget.b_remove.clicked.emit()
        assert len(self.test_obj.rotor.hole) == 2
        assert type(self.test_obj.rotor.hole[1]) == HoleM50
        assert self.widget.tab_hole.count() == 2

        self.widget.b_remove.clicked.emit()
        assert len(self.test_obj.rotor.hole) == 1
        assert self.widget.tab_hole.count() == 1

        # There is always at least 1 hole
        self.widget.b_remove.clicked.emit()
        assert len(self.test_obj.rotor.hole) == 1
        assert self.widget.tab_hole.count() == 1

    def test_add_remove_hole_SyRM(self):
        assert len(self.test_obj2.rotor.hole) == 1
        assert self.widget2.tab_hole.count() == 1

        self.widget2.b_add.clicked.emit()

        assert len(self.test_obj2.rotor.hole) == 2
        assert type(self.test_obj2.rotor.hole[1]) == HoleM50
        assert self.test_obj2.rotor.hole[1].Zh == 16
        assert self.test_obj2.rotor.hole[1].magnet_0 == None
        assert self.widget2.tab_hole.count() == 2

        self.widget2.b_remove.clicked.emit()
        assert len(self.test_obj2.rotor.hole) == 1
        assert self.widget2.tab_hole.count() == 1

        # There is always at least 1 hole
        self.widget2.b_remove.clicked.emit()
        assert len(self.test_obj2.rotor.hole) == 1
        assert self.widget2.tab_hole.count() == 1
