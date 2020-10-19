# -*- coding: utf-8 -*-

import sys

from PySide2 import QtWidgets

from pyleecan.Classes.MatMagnetics import MatMagnetics
from pyleecan.Classes.Material import Material
from pyleecan.GUI.Dialog.DMatLib.DMatLib import DMatLib
from pyleecan.GUI.Dialog.DMatLib.MatLib import MatLib
from Tests import save_gui_path

from os import makedirs
from os.path import isdir, join
from shutil import rmtree

import pytest

# To save the tmp Matlib
tmp_folder = join(save_gui_path, "DMatLib", "tmp_matlib")


@pytest.mark.GUI
class TestDMatLib(object):
    """Test that the widget DMatLib behave like it should"""

    def setup_method(self, method):
        """Run at the begining of every test to setup the gui"""
        mat_lib = list()
        mat_lib.append(Material())
        mat_lib[0].name = "test_material_1"
        mat_lib[0].is_isotropic = True
        mat_lib[0].elec.rho = 0.11
        mat_lib[0].mag = MatMagnetics(mur_lin=0.12, Wlam=0.13)
        mat_lib[0].struct.rho = 0.14
        mat_lib[0].struct.Ex = 0.15
        mat_lib[0].struct.Ey = 0.152
        mat_lib[0].struct.Ez = 0.153
        mat_lib[0].struct.nu_xy = 0.16
        mat_lib[0].struct.nu_yz = 0.162
        mat_lib[0].struct.nu_xz = 0.163
        mat_lib[0].struct.Gxy = 0.17
        mat_lib[0].struct.Gyz = 0.172
        mat_lib[0].struct.Gxz = 0.173
        mat_lib[0].HT.lambda_x = 0.18
        mat_lib[0].HT.lambda_y = 0.182
        mat_lib[0].HT.lambda_z = 0.183
        mat_lib[0].HT.Cp = 0.19
        mat_lib[0].HT.alpha = 0.20
        mat_lib[0].eco.cost_unit = 0.21

        mat_lib.append(Material(name="test_material_2"))
        mat_lib.append(Material(name="test_material_3"))
        mat_lib.append(Material(name="test_material_4"))
        mat_lib.append(Material(name="test_material_5"))
        mat_lib.append(Material(name="test_material_6"))
        mat_lib.append(Material(name="test_material_7"))

        matlib = MatLib()
        matlib.dict_mat["RefMatLib"] = mat_lib
        matlib.index_first_mat_mach = 7

        # Save material in a tmp folder
        if isdir(tmp_folder):
            rmtree(tmp_folder)
        makedirs(tmp_folder)
        for mat in mat_lib:
            mat.save(tmp_folder + "/" + mat.name + ".json")

        self.widget = DMatLib(matlib)

    @classmethod
    def setUpClass(cls):
        """Start the app for the test"""
        print("\nStart Test DMatLib")
        if not QtWidgets.QApplication.instance():
            cls.app = QtWidgets.QApplication(sys.argv)
        else:
            cls.app = QtWidgets.QApplication.instance()

    @classmethod
    def tearDownClass(cls):
        """Exit the app after the test"""
        cls.app.quit()
        rmtree(tmp_folder)

    def test_init(self):
        """Check that the Widget spinbox initialise to the lamination value"""
        assert self.widget.out_name.text() == "name: test_material_1"
        assert self.widget.out_iso.text() == "type: isotropic"
        assert self.widget.out_rho_elec.text() == "rho = 0.11 ohm.m"
        assert self.widget.out_cost_unit.text() == u"cost_unit = 0.21 €/kg"
        assert self.widget.out_Cp.text() == "Cp = 0.19 W/kg/K"
        assert self.widget.out_alpha.text() == "alpha = 0.2"
        assert self.widget.out_L.text() == "Lambda = 0.18 W/K"
        assert self.widget.out_rho_meca.text() == "rho = 0.14 kg/m^3"
        assert self.widget.out_E.text() == "E = 0.15 Pa"
        assert self.widget.out_G.text() == "G = 0.17 Pa"
        assert self.widget.out_nu.text() == "nu = 0.16"
        assert self.widget.out_mur_lin.text() == "mur_lin = 0.12"
        assert self.widget.out_wlam.text() == "wlam = 0.13 m"

        # Check list
        assert self.widget.nav_mat.count() == 7
        for ii in range(0, self.widget.nav_mat.count()):
            assert self.widget.nav_mat.item(ii).text() == "00" + str(
                ii + 1
            ) + " - test_material_" + str(ii + 1)
