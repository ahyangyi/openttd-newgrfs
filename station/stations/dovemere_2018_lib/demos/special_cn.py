from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

special_demo_cn = Demo(
    "Irregular 7×7 station layout",
    [
        [corner.T, front_gate.T, front_gate.T.R, funnel.T.R, h_normal_corridor, h_normal_corridor, h_end_corridor.R],
        [side_a2, central_windowed, central_windowed.R, side_a3.T.R, platform, platform, platform],
        [corner, inner_corner, central, side_a3.R, platform, platform, platform],
        [None, corner, front_normal, double_corner.R, front_normal.T, corner.T.R, None],
        [platform, platform, platform, side_a3.T, central, inner_corner.T.R, corner.T.R],
        [platform, platform, platform, side_a3, central_windowed, central_windowed.R, side_a2.R],
        [h_end_corridor, h_normal_corridor, h_normal_corridor, funnel, front_gate, front_gate.R, corner.R],
    ],
    remap=get_1cc_remap(CompanyColour.MAUVE),
)
