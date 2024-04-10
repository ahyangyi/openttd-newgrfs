from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

rail_near = [platform_s, v_central_n, platform_s, platform_s, platform_s, v_central_n, platform_s]
rail_far = [x.T for x in rail_near]
rail_both = [platform, v_central, platform, platform, platform, v_central, platform]
station = [
    h_end_asym_platform,
    junction3,
    h_gate_1_platform,
    h_gate_extender,
    h_gate_1_platform.R,
    junction3,
    h_end_asym_platform.R,
]

special_demo_g = Demo(
    "Irregular 7×7 station layout",
    [[x.T for x in station], rail_far, rail_near, rail_both, rail_far, rail_near, station],
    remap=get_1cc_remap(CompanyColour.YELLOW),
)
