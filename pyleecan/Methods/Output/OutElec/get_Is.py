from ....Functions.Electrical.coordinate_transformation import dq2n
from numpy import pi, array, transpose
from SciDataTool import Data1D, DataTime
from ....Functions.Winding.gen_phase_list import gen_name


def get_Is(self):
    """Return the stator current"""
    if self.Is is None:
        # Generate current according to Id/Iq
        Isdq = array([self.Id_ref, self.Iq_ref])
        time = self.time.get_values(is_oneperiod=True)
        qs = self.parent.simu.machine.stator.winding.qs
        felec = self.felec

        # Get rotation direction of the fundamental magnetic field created by the winding
        rot_dir = self.parent.get_rot_dir()

        # Get stator current function of time
        Is = dq2n(Isdq, 2 * pi * felec * time, n=qs, rot_dir=rot_dir, is_n_rms=False)

        Time = self.time
        Phase = Data1D(
            name="phase",
            unit="",
            values=gen_name(qs, is_add_phase=True),
            is_components=True,
        )
        self.Is = DataTime(
            name="Stator current",
            unit="A",
            symbol="Is",
            axes=[Phase, Time],
            symmetries=self.time.symmetries,
            values=transpose(Is),
        )
    return self.Is
