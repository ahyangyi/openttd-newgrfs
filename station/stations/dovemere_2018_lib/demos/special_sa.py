from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

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
            bicorner_2.TR,
        ],
        [platform_s_nt.T.M, platform_s.M, platform_s.T.M, platform_s.M, corner.R.M, double_corner_2, v_funnel_2.R],
        [platform_s_nt.T.M, platform_s.M, platform_s.T.M, corner.R.M, double_corner_2, corner.R, v_central_n.T],
        [platform_s_nt.T.M, platform_s.M, corner.R.M, double_corner_2, corner.R, platform_s, v_central_n],
        [platform_s_nt.T.M, corner.R.M, double_corner_2, corner.R, platform_s.T, platform_s.T, v_central_n.T],
        [corner_gate.R.M, double_corner_2, corner.R, platform_s, platform_s, platform_s, v_central_n],
        [
            front_gate_extender_corner,
            corner_gate.R,
            platform_s_nt.T,
            platform_s_nt.T,
            platform_s_nt.T,
            platform_s_nt.T,
            v_end_platform,
        ],
    ],
    remap=get_1cc_remap(CompanyColour.PURPLE),
)
