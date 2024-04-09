from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

special_demo_cp = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end, junction3.T, h_normal, turn.TR, None, None, None],
        [platform, v_central, platform, v_central, platform, platform, platform],
        [platform, v_central, platform, v_central, platform, platform, platform],
        [platform, v_central, platform, v_central, corner.T, front_normal.T, corner.T.R],
        [platform, v_end_platform, platform, turn, double_inner_corner, central_windowed_extender, side_a2_windowed.R],
        [None, None, None, None, v_funnel, front_normal, corner.R],
        [None, None, None, None, v_end_gate, None, None],
    ],
    remap=get_1cc_remap(CompanyColour.CREAM),
)
