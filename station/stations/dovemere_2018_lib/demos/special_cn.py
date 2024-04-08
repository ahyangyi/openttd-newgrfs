from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

special_demo_cn = Demo(
    "Irregular 7×7 station layout",
    [
        [corner.T, front_gate.T, front_gate.TR, funnel.TR, h_normal, h_normal, h_end.R],
        [side_a2, central_windowed, central_windowed.R, side_a3.TR, platform, platform, platform],
        [corner, inner_corner, central, side_a3.R, platform, platform, platform],
        [None, corner, front_normal, double_corner.R, front_normal.T, corner.TR, None],
        [platform, platform, platform, side_a3.T, central, inner_corner.TR, corner.TR],
        [platform, platform, platform, side_a3, central_windowed, central_windowed.R, side_a2.R],
        [h_end, h_normal, h_normal, funnel, front_gate, front_gate.R, corner.R],
    ],
    remap=get_1cc_remap(CompanyColour.MAUVE),
)
