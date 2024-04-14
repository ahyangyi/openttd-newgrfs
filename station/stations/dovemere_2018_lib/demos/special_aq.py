from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

rail_row = [platform_s_nt.T.M, platform_s.M, platform_s.T.M, platform.M, platform_s.M, platform_s.T.M, platform_s_nt.M]
top_building = [
    corner_gate_platform.R.M,
    side_a3_windowed_f.R.M,
    side_a3_windowed_f.TR.M,
    side_a3_windowed.R.M,
    side_a3_windowed_f.TR.M,
    side_a2_windowed_n.TR.M,
    corner_gate_platform.TR.M,
]
bottom_building = [
    corner_gate_platform.M,
    side_a2_windowed_n.M,
    side_a3_windowed_f.M,
    side_a3_windowed.T.M,
    side_a3_windowed_n.M,
    side_a3_windowed_n.T.M,
    corner_gate_platform.T.M,
]

special_demo_aq = Demo(
    "Irregular 7×7 station layout",
    [rail_row, top_building, bottom_building, rail_row, top_building, bottom_building, rail_row],
    remap=get_1cc_remap(CompanyColour.LIGHT_BLUE),
)
