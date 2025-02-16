from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_1")

nt = concourse

special_demo_sa = Demo(
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
        [nt.T.M, cns.M, cns.T.M, cns.M, corner.R.M, double_corner_2, v_funnel_2.R],
        [nt.T.M, cns.M, cns.T.M, corner.R.M, double_corner_2, corner.R, v_central_n.T],
        [nt.T.M, cns.M, corner.R.M, double_corner_2, corner.R, cns, v_central_n],
        [nt.T.M, corner.R.M, double_corner_2, corner.R, cns.T, cns.T, v_central_n.T],
        [corner_gate.R.M, double_corner_2, corner.R, cns, cns, cns, v_central_n],
        [front_gate_extender_corner, corner_gate.R, nt.T, nt.T, nt.T, nt.T, v_end_platform],
    ],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.PURPLE),
    climate="tropical",
    subclimate="desert",
)
