from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform, platform_s
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = platform_tiles.concourse_side_shelter

special_demo_cp = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end_corridor, tee.T, h_normal_corridor, turn.T.R, None, None, None],
        [platform_s, v_central_n, platform_s, v_central_n, platform, platform, platform],
        [platform_s.T, v_central_n.T, platform_s.T, v_central_n.T, platform, platform, platform],
        [platform_s, v_central_n, platform_s, v_central_n, corner.T, front_normal.T, corner.T.R],
        [nt.T, v_end_platform, nt.T, turn, double_inner_corner, central_windowed_extender, side_a2_windowed.R],
        [None, None, None, None, v_funnel, front_normal, corner.R],
        [None, None, None, None, v_end_gate, None, None],
    ],
    remap=get_1cc_remap(CompanyColour.CREAM),
)
