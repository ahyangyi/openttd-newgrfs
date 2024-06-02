from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d
from station.stations.platforms import concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

top_half = [
    [corner.T, front_gate.T, front_gate.T.R, funnel.T.R, h_normal_corridor, h_normal_corridor, h_end_corridor.R],
    [side_a2_d, central_windowed_d, central_windowed_d.R, side_a3_d.T.R, platform_d, platform_d, platform_d],
    [corner, inner_corner, central_d, side_a3_d.R, platform_d, platform_d, platform_d],
    [concourse, corner, front_normal, double_corner.R, front_normal.T, corner.T.R, concourse],
]

special_demo_cn = Demo(
    "Irregular 7×7 station layout",
    top_half + [[i and i.T.R for i in row[::-1]] for row in top_half[2::-1]],
    remap=get_1cc_remap(CompanyColour.MAUVE),
    climate="temperate",
)
