from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_2")

rail_row = [concourse.T.M, cns.M, cns.T.M, cns_d.M, cns.M, cns.T.M, concourse.M]
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
    [rail_row, top_building, bottom_building, rail_row, top_building, bottom_building, rail_row],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.LIGHT_BLUE),
    climate="arctic",
    subclimate="snow",
)
