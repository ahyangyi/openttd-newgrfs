from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_2")

top_half = [
    [default, h_end_asym_gate.T, turn_gate.T.R, concourse_none, turn_gate.T, h_end_asym_gate.T.R, default],
    [cns, cns, v_central_n, cns, v_central_n, cns, cns],
    [cns.T, cns.T, v_central_n.T, cns.T, v_central_n.T, cns.T, cns.T],
    [
        h_end_corridor,
        h_normal_corridor,
        cross_corridor,
        h_normal_corridor,
        cross_corridor,
        h_normal_corridor,
        h_end_corridor.R,
    ],
]

special_demo_p = Demo(
    top_half + [[i and i.T for i in row] for row in top_half[2::-1]],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.PALE_GREEN),
    climate="tropical",
)
