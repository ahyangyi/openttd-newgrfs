from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="brick", shelter_class="shelter_2")

rail_near = [cns, v_central_n, cns, cns, cns, v_central_n, cns]
rail_far = [x.T for x in rail_near]
rail_both = [cns_d, v_central_d, cns_d, cns_d, cns_d, v_central_d, cns_d]
station = [
    h_end_asym_platform,
    tee_platform,
    h_gate_1_platform,
    h_gate_extender_1_platform,
    h_gate_1_platform.R,
    tee_platform,
    h_end_asym_platform.R,
]

special_demo_g = Demo(
    [[x.T for x in station], rail_far, rail_near, rail_both, rail_far, rail_near, station],
    "Irregular 7×7 station layout",
    remap=get_1cc_remap(CompanyColour.YELLOW),
    climate="arctic",
)
