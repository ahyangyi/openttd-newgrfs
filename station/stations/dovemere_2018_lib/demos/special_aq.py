from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d, platform_n
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = platform_tiles.concourse_side_shelter_1

rail_row = [nt.T.M, platform_n.M, platform_n.T.M, platform_d.M, platform_n.M, platform_n.T.M, nt.M]
top_building = [
    corner_gate_platform.R.M,
    side_a3_windowed_f.R.M,
    side_a3_windowed_f.T.R.M,
    side_a3_windowed_d.R.M,
    side_a3_windowed_f.T.R.M,
    side_a2_windowed_n.T.R.M,
    corner_gate_platform.T.R.M,
]
bottom_building = [
    corner_gate_platform.M,
    side_a2_windowed_n.M,
    side_a3_windowed_f.M,
    side_a3_windowed_d.T.M,
    side_a3_windowed_n.M,
    side_a3_windowed_n.T.M,
    corner_gate_platform.T.M,
]

special_demo_aq = Demo(
    "Irregular 7×7 station layout",
    [rail_row, top_building, bottom_building, rail_row, top_building, bottom_building, rail_row],
    remap=get_1cc_remap(CompanyColour.LIGHT_BLUE),
    climate="arctic",
    subclimate="snow",
)
