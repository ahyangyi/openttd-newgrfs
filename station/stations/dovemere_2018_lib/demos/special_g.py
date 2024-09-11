from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles
from station.stations.platforms import cns_brick_d, cns_brick
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

rail_near = [cns_brick, v_central_brick_n, cns_brick, cns_brick, cns_brick, v_central_brick_n, cns_brick]
rail_far = [x.T for x in rail_near]
rail_both = [cns_brick_d, v_central_brick_d, cns_brick_d, cns_brick_d, cns_brick_d, v_central_brick_d, cns_brick_d]
station = [
    h_end_asym_brick_platform,
    tee_brick_platform,
    h_gate_1_brick_platform,
    h_gate_extender_1_brick_platform,
    h_gate_1_brick_platform.R,
    tee_brick_platform,
    h_end_asym_brick_platform.R,
]

special_demo_g = Demo(
    "Irregular 7×7 station layout",
    [[x.T for x in station], rail_far, rail_near, rail_both, rail_far, rail_near, station],
    remap=get_1cc_remap(CompanyColour.YELLOW),
    climate="arctic",
)
