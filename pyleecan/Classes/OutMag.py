# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Output/OutMag.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Output/OutMag
"""

from os import linesep
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

from numpy import array, array_equal
from ._check import InitUnKnowClassError
from .MeshSolution import MeshSolution


class OutMag(FrozenClass):
    """Gather the magnetic module outputs"""

    VERSION = 1

    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        time=None,
        angle=None,
        B=None,
        Tem=None,
        Tem_av=None,
        Tem_rip_norm=None,
        Tem_rip_pp=None,
        Phi_wind_stator=None,
        emf=None,
        meshsolution=-1,
        FEMM_dict=None,
        logger_name="Pyleecan.OutMag",
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for pyleecan type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "time" in list(init_dict.keys()):
                time = init_dict["time"]
            if "angle" in list(init_dict.keys()):
                angle = init_dict["angle"]
            if "B" in list(init_dict.keys()):
                B = init_dict["B"]
            if "Tem" in list(init_dict.keys()):
                Tem = init_dict["Tem"]
            if "Tem_av" in list(init_dict.keys()):
                Tem_av = init_dict["Tem_av"]
            if "Tem_rip_norm" in list(init_dict.keys()):
                Tem_rip_norm = init_dict["Tem_rip_norm"]
            if "Tem_rip_pp" in list(init_dict.keys()):
                Tem_rip_pp = init_dict["Tem_rip_pp"]
            if "Phi_wind_stator" in list(init_dict.keys()):
                Phi_wind_stator = init_dict["Phi_wind_stator"]
            if "emf" in list(init_dict.keys()):
                emf = init_dict["emf"]
            if "meshsolution" in list(init_dict.keys()):
                meshsolution = init_dict["meshsolution"]
            if "FEMM_dict" in list(init_dict.keys()):
                FEMM_dict = init_dict["FEMM_dict"]
            if "logger_name" in list(init_dict.keys()):
                logger_name = init_dict["logger_name"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.time = time
        self.angle = angle
        self.B = B
        self.Tem = Tem
        self.Tem_av = Tem_av
        self.Tem_rip_norm = Tem_rip_norm
        self.Tem_rip_pp = Tem_rip_pp
        self.Phi_wind_stator = Phi_wind_stator
        self.emf = emf
        self.meshsolution = meshsolution
        self.FEMM_dict = FEMM_dict
        self.logger_name = logger_name

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        OutMag_str = ""
        if self.parent is None:
            OutMag_str += "parent = None " + linesep
        else:
            OutMag_str += "parent = " + str(type(self.parent)) + " object" + linesep
        OutMag_str += "time = " + str(self.time) + linesep + linesep
        OutMag_str += "angle = " + str(self.angle) + linesep + linesep
        OutMag_str += "B = " + str(self.B) + linesep + linesep
        OutMag_str += "Tem = " + str(self.Tem) + linesep + linesep
        OutMag_str += "Tem_av = " + str(self.Tem_av) + linesep
        OutMag_str += "Tem_rip_norm = " + str(self.Tem_rip_norm) + linesep
        OutMag_str += "Tem_rip_pp = " + str(self.Tem_rip_pp) + linesep
        OutMag_str += (
            "Phi_wind_stator = " + str(self.Phi_wind_stator) + linesep + linesep
        )
        OutMag_str += (
            "emf = "
            + linesep
            + str(self.emf).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        if self.meshsolution is not None:
            tmp = (
                self.meshsolution.__str__()
                .replace(linesep, linesep + "\t")
                .rstrip("\t")
            )
            OutMag_str += "meshsolution = " + tmp
        else:
            OutMag_str += "meshsolution = None" + linesep + linesep
        OutMag_str += "FEMM_dict = " + str(self.FEMM_dict) + linesep
        OutMag_str += 'logger_name = "' + str(self.logger_name) + '"' + linesep
        return OutMag_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.time != self.time:
            return False
        if other.angle != self.angle:
            return False
        if other.B != self.B:
            return False
        if other.Tem != self.Tem:
            return False
        if other.Tem_av != self.Tem_av:
            return False
        if other.Tem_rip_norm != self.Tem_rip_norm:
            return False
        if other.Tem_rip_pp != self.Tem_rip_pp:
            return False
        if other.Phi_wind_stator != self.Phi_wind_stator:
            return False
        if not array_equal(other.emf, self.emf):
            return False
        if other.meshsolution != self.meshsolution:
            return False
        if other.FEMM_dict != self.FEMM_dict:
            return False
        if other.logger_name != self.logger_name:
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        OutMag_dict = dict()
        if self.time is None:
            OutMag_dict["time"] = None
        else:
            OutMag_dict["time"] = self.time.as_dict()
        if self.angle is None:
            OutMag_dict["angle"] = None
        else:
            OutMag_dict["angle"] = self.angle.as_dict()
        if self.B is None:
            OutMag_dict["B"] = None
        else:
            OutMag_dict["B"] = self.B.as_dict()
        if self.Tem is None:
            OutMag_dict["Tem"] = None
        else:
            OutMag_dict["Tem"] = self.Tem.as_dict()
        OutMag_dict["Tem_av"] = self.Tem_av
        OutMag_dict["Tem_rip_norm"] = self.Tem_rip_norm
        OutMag_dict["Tem_rip_pp"] = self.Tem_rip_pp
        if self.Phi_wind_stator is None:
            OutMag_dict["Phi_wind_stator"] = None
        else:
            OutMag_dict["Phi_wind_stator"] = self.Phi_wind_stator.as_dict()
        if self.emf is None:
            OutMag_dict["emf"] = None
        else:
            OutMag_dict["emf"] = self.emf.tolist()
        if self.meshsolution is None:
            OutMag_dict["meshsolution"] = None
        else:
            OutMag_dict["meshsolution"] = self.meshsolution.as_dict()
        OutMag_dict["FEMM_dict"] = (
            self.FEMM_dict.copy() if self.FEMM_dict is not None else None
        )
        OutMag_dict["logger_name"] = self.logger_name
        # The class name is added to the dict for deserialisation purpose
        OutMag_dict["__class__"] = "OutMag"
        return OutMag_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.time = None
        self.angle = None
        self.B = None
        self.Tem = None
        self.Tem_av = None
        self.Tem_rip_norm = None
        self.Tem_rip_pp = None
        self.Phi_wind_stator = None
        self.emf = None
        if self.meshsolution is not None:
            self.meshsolution._set_None()
        self.FEMM_dict = None
        self.logger_name = None

    def _get_time(self):
        """getter of time"""
        return self._time

    def _set_time(self, value):
        """setter of time"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "SciDataTool.Classes", value.get("__class__"), "time"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = Data()
        check_var("time", value, "Data")
        self._time = value

    time = property(
        fget=_get_time,
        fset=_set_time,
        doc=u"""Magnetic time vector (no symmetry)

        :Type: SciDataTool.Classes.DataND.Data
        """,
    )

    def _get_angle(self):
        """getter of angle"""
        return self._angle

    def _set_angle(self, value):
        """setter of angle"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "SciDataTool.Classes", value.get("__class__"), "angle"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = Data()
        check_var("angle", value, "Data")
        self._angle = value

    angle = property(
        fget=_get_angle,
        fset=_set_angle,
        doc=u"""Magnetic position vector (no symmetry)

        :Type: SciDataTool.Classes.DataND.Data
        """,
    )

    def _get_B(self):
        """getter of B"""
        return self._B

    def _set_B(self, value):
        """setter of B"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class("SciDataTool.Classes", value.get("__class__"), "B")
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = VectorField()
        check_var("B", value, "VectorField")
        self._B = value

    B = property(
        fget=_get_B,
        fset=_set_B,
        doc=u"""Airgap flux density components

        :Type: SciDataTool.Classes.VectorField.VectorField
        """,
    )

    def _get_Tem(self):
        """getter of Tem"""
        return self._Tem

    def _set_Tem(self, value):
        """setter of Tem"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "SciDataTool.Classes", value.get("__class__"), "Tem"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = DataND()
        check_var("Tem", value, "DataND")
        self._Tem = value

    Tem = property(
        fget=_get_Tem,
        fset=_set_Tem,
        doc=u"""Electromagnetic torque

        :Type: SciDataTool.Classes.DataND.DataND
        """,
    )

    def _get_Tem_av(self):
        """getter of Tem_av"""
        return self._Tem_av

    def _set_Tem_av(self, value):
        """setter of Tem_av"""
        check_var("Tem_av", value, "float")
        self._Tem_av = value

    Tem_av = property(
        fget=_get_Tem_av,
        fset=_set_Tem_av,
        doc=u"""Average Electromagnetic torque

        :Type: float
        """,
    )

    def _get_Tem_rip_norm(self):
        """getter of Tem_rip_norm"""
        return self._Tem_rip_norm

    def _set_Tem_rip_norm(self, value):
        """setter of Tem_rip_norm"""
        check_var("Tem_rip_norm", value, "float")
        self._Tem_rip_norm = value

    Tem_rip_norm = property(
        fget=_get_Tem_rip_norm,
        fset=_set_Tem_rip_norm,
        doc=u"""Peak to Peak Torque ripple normalized according to average torque (None if average torque=0)

        :Type: float
        """,
    )

    def _get_Tem_rip_pp(self):
        """getter of Tem_rip_pp"""
        return self._Tem_rip_pp

    def _set_Tem_rip_pp(self, value):
        """setter of Tem_rip_pp"""
        check_var("Tem_rip_pp", value, "float")
        self._Tem_rip_pp = value

    Tem_rip_pp = property(
        fget=_get_Tem_rip_pp,
        fset=_set_Tem_rip_pp,
        doc=u"""Peak to Peak Torque ripple

        :Type: float
        """,
    )

    def _get_Phi_wind_stator(self):
        """getter of Phi_wind_stator"""
        return self._Phi_wind_stator

    def _set_Phi_wind_stator(self, value):
        """setter of Phi_wind_stator"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "SciDataTool.Classes", value.get("__class__"), "Phi_wind_stator"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = DataTime()
        check_var("Phi_wind_stator", value, "DataTime")
        self._Phi_wind_stator = value

    Phi_wind_stator = property(
        fget=_get_Phi_wind_stator,
        fset=_set_Phi_wind_stator,
        doc=u"""Stator winding flux

        :Type: SciDataTool.Classes.DataTime.DataTime
        """,
    )

    def _get_emf(self):
        """getter of emf"""
        return self._emf

    def _set_emf(self, value):
        """setter of emf"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("emf", value, "ndarray")
        self._emf = value

    emf = property(
        fget=_get_emf,
        fset=_set_emf,
        doc=u"""Electromotive force

        :Type: ndarray
        """,
    )

    def _get_meshsolution(self):
        """getter of meshsolution"""
        return self._meshsolution

    def _set_meshsolution(self, value):
        """setter of meshsolution"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "pyleecan.Classes", value.get("__class__"), "meshsolution"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = MeshSolution()
        check_var("meshsolution", value, "MeshSolution")
        self._meshsolution = value

        if self._meshsolution is not None:
            self._meshsolution.parent = self

    meshsolution = property(
        fget=_get_meshsolution,
        fset=_set_meshsolution,
        doc=u"""FEA software mesh and solution

        :Type: MeshSolution
        """,
    )

    def _get_FEMM_dict(self):
        """getter of FEMM_dict"""
        return self._FEMM_dict

    def _set_FEMM_dict(self, value):
        """setter of FEMM_dict"""
        if type(value) is int and value == -1:
            value = dict()
        check_var("FEMM_dict", value, "dict")
        self._FEMM_dict = value

    FEMM_dict = property(
        fget=_get_FEMM_dict,
        fset=_set_FEMM_dict,
        doc=u"""Dictionnary containing the main FEMM parameter

        :Type: dict
        """,
    )

    def _get_logger_name(self):
        """getter of logger_name"""
        return self._logger_name

    def _set_logger_name(self, value):
        """setter of logger_name"""
        check_var("logger_name", value, "str")
        self._logger_name = value

    logger_name = property(
        fget=_get_logger_name,
        fset=_set_logger_name,
        doc=u"""Name of the logger to use

        :Type: str
        """,
    )
