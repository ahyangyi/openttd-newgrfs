from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

special_demo_cn = Demo(
    "Irregular 7×7 station layout",
    [
        [corner.T, front_gate.T, front_gate.T.R, funnel.T.R, h_normal_corridor, h_normal_corridor, h_end_corridor.R],
        [side_a2_d, central_windowed_d, central_windowed_d.R, side_a3_d.T.R, platform_d, platform_d, platform_d],
        [corner, inner_corner, central_d, side_a3_d.R, platform_d, platform_d, platform_d],
        [None, corner, front_normal, double_corner.R, front_normal.T, corner.T.R, None],
        [platform_d, platform_d, platform_d, side_a3_d.T, central_d, inner_corner.T.R, corner.T.R],
        [platform_d, platform_d, platform_d, side_a3_d, central_windowed_d, central_windowed_d.R, side_a2_d.R],
        [h_end_corridor, h_normal_corridor, h_normal_corridor, funnel, front_gate, front_gate.R, corner.R],
    ],
    remap=get_1cc_remap(CompanyColour.MAUVE),
)
