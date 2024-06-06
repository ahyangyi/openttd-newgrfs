from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d, platform_n
from station.stations.platforms import concourse
from station.stations.misc import default
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = platform_tiles.concourse_side_shelter_1

special_demo_cp = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end_corridor, tee.T, h_normal_corridor, turn.T.R, default, default, default],
        [platform_n, v_central_n, platform_n, v_central_n, platform_d, platform_d, platform_d],
        [platform_n.T, v_central_n.T, platform_n.T, v_central_n.T, platform_d, platform_d, platform_d],
        [platform_n, v_central_n, platform_n, v_central_n, corner.T, front_normal.T, corner.T.R],
        [nt.T, v_end_platform, nt.T, turn, double_inner_corner, central_windowed_extender_d, side_a2_windowed_d.R],
        [concourse, concourse, concourse, concourse, v_funnel, front_normal, corner.R],
        [default, default, default, default, v_end_gate, default, default],
    ],
    remap=get_1cc_remap(CompanyColour.CREAM),
    climate="toyland",
)
