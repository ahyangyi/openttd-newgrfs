from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_n
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = platform_tiles.concourse_side_shelter_1

special_demo_sa = Demo(
    "Irregular 7×7 station layout",
    [
        [
            v_end_platform.M,
            v_central_n.M,
            v_central_n.T.M,
            v_central_n.M,
            v_central_n.T.M,
            v_funnel_2.R.M,
            bicorner_2.T.R,
        ],
        [nt.T.M, platform_n.M, platform_n.T.M, platform_n.M, corner.R.M, double_corner_2, v_funnel_2.R],
        [nt.T.M, platform_n.M, platform_n.T.M, corner.R.M, double_corner_2, corner.R, v_central_n.T],
        [nt.T.M, platform_n.M, corner.R.M, double_corner_2, corner.R, platform_n, v_central_n],
        [nt.T.M, corner.R.M, double_corner_2, corner.R, platform_n.T, platform_n.T, v_central_n.T],
        [corner_gate.R.M, double_corner_2, corner.R, platform_n, platform_n, platform_n, v_central_n],
        [front_gate_extender_corner, corner_gate.R, nt.T, nt.T, nt.T, nt.T, v_end_platform],
    ],
    remap=get_1cc_remap(CompanyColour.PURPLE),
    climate="tropical",
    subclimate="desert",
)
