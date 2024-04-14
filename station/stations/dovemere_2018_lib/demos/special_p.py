from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

special_demo_p = Demo(
    "Irregular 7×7 station layout",
    [
        [None, h_end_asym_gate.T, turn_gate.TR, None, turn_gate.T, h_end_asym_gate.TR, None],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [h_end, h_windowed, cross, h_windowed_extender, cross, h_windowed.R, h_end.R],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [None, h_end_asym_gate, turn_gate.R, None, turn_gate, h_end_asym_gate.R, None],
    ],
    remap=get_1cc_remap(CompanyColour.PALE_GREEN),
)
