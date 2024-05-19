from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_d, platform_n
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

rail_near = [platform_n, v_central_n, platform_n, platform_n, platform_n, v_central_n, platform_n]
rail_far = [x.T for x in rail_near]
rail_both = [platform_d, v_central, platform_d, platform_d, platform_d, v_central, platform_d]
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
    "Irregular 7×7 station layout",
    [[x.T for x in station], rail_far, rail_near, rail_both, rail_far, rail_near, station],
    remap=get_1cc_remap(CompanyColour.YELLOW),
)
