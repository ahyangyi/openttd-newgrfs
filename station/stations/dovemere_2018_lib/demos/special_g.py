from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

near = [platform_s, v_central_n, platform_s, platform_s, platform_s, v_central_n, platform_s]
far = [x.T for x in near]
both = [platform, v_central, platform, platform, platform, v_central, platform]

special_demo_g = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end_asym.T, junction3.T, h_windowed, h_windowed_extender, h_windowed.R, junction3.T, h_end_asym.TR],
        far,
        near,
        both,
        far,
        near,
        [h_end_asym, junction3, h_gate, h_gate_extender, h_gate.R, junction3, h_end_asym.R],
    ],
    remap=get_1cc_remap(CompanyColour.YELLOW),
)
