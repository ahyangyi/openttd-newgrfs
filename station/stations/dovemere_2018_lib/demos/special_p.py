from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_n
from station.stations.platforms import concourse
from station.stations.misc import default
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
top_half = [
    [default, h_end_asym_gate.T, turn_gate.T.R, concourse, turn_gate.T, h_end_asym_gate.T.R, default],
    [platform_n, platform_n, v_central_n, platform_n, v_central_n, platform_n, platform_n],
    [platform_n.T, platform_n.T, v_central_n.T, platform_n.T, v_central_n.T, platform_n.T, platform_n.T],
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
    "Irregular 7×7 station layout",
    top_half + [[i and i.T for i in row] for row in top_half[2::-1]],
    remap=get_1cc_remap(CompanyColour.PALE_GREEN),
    climate="tropical",
)
