from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_2")

special_demo_cp = Demo(
    [
        [h_end_corridor, tee.T, h_normal_corridor, turn.T.R, default, default, default],
        [cns, v_central_n, cns, v_central_n, cns_d, cns_d, cns_d],
        [cns.T, v_central_n.T, cns.T, v_central_n.T, cns_d, cns_d, cns_d],
        [cns, v_central_n, cns, v_central_n, corner.T, front_normal.T, corner.T.R],
        [
            concourse.T,
            v_end_platform,
            concourse.T,
            turn,
            double_inner_corner,
            central_windowed_extender_d,
            side_a2_windowed_d.R,
        ],
        [concourse_none, concourse_none, concourse_none, concourse_none, v_funnel, front_normal, corner.R],
        [default, default, default, default, v_end_gate, default, default],
    ],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.CREAM),
    climate="toyland",
)
