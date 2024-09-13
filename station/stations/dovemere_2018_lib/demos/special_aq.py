from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d, platform_n
from station.stations.platforms import cns_shelter_2, cns_shelter_2_d, concourse_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = concourse_tiles.shelter_2

rail_row = [nt.T.M, cns_shelter_2.M, cns_shelter_2.T.M, cns_shelter_2_d.M, cns_shelter_2.M, cns_shelter_2.T.M, nt.M]
top_building = [
    corner_gate_shelter_2_platform.R.M,
    side_a3_windowed_shelter_2_f.R.M,
    side_a3_windowed_shelter_2_f.T.R.M,
    side_a3_windowed_shelter_2_d.R.M,
    side_a3_windowed_shelter_2_f.T.R.M,
    side_a2_windowed_shelter_2_n.T.R.M,
    corner_gate_shelter_2_platform.T.R.M,
]
bottom_building = [
    corner_gate_shelter_2_platform.M,
    side_a2_windowed_shelter_2_n.M,
    side_a3_windowed_shelter_2_f.M,
    side_a3_windowed_shelter_2_d.T.M,
    side_a3_windowed_shelter_2_n.M,
    side_a3_windowed_shelter_2_n.T.M,
    corner_gate_shelter_2_platform.T.M,
]

special_demo_aq = Demo(
    "Irregular 7×7 station layout",
    [rail_row, top_building, bottom_building, rail_row, top_building, bottom_building, rail_row],
    remap=get_1cc_remap(CompanyColour.LIGHT_BLUE),
    climate="arctic",
    subclimate="snow",
)
