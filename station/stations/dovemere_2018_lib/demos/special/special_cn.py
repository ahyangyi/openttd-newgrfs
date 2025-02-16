from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_1")

top_half = [
    [
        corner_third.T,
        front_gate_third.T,
        front_gate_third.T.R,
        funnel.T.R,
        h_normal_corridor,
        h_normal_corridor,
        h_end_corridor.R,
    ],
    [side_a2_n, central_windowed_n, central_windowed_n.R, side_a3_f.T.R, cns, cns, cns],
    [corner_third_f, inner_corner, central_f, side_a3_f.R, cns.T, cns.T, cns.T],
    [concourse_none, corner, front_normal, double_corner.R, front_normal.T, corner.T.R, concourse],
]

special_demo_cn = Demo(
    top_half + [[i and i.T.R for i in row[::-1]] for row in top_half[2::-1]],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.MAUVE),
    climate="temperate",
)
