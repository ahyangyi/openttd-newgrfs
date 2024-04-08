from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

special_demo_sa = Demo(
    "Irregular 7×7 station layout",
    [
        [v_end.M, v_central.M, v_central.M, v_central.M, v_central.M, v_funnel.R.M, bicorner.TR],
        [platform.M, platform.M, platform.M, platform.M, corner.R.M, double_corner_2, v_funnel.R],
        [platform.M, platform.M, platform.M, corner.R.M, double_corner_2, corner.R, v_central],
        [platform.M, platform.M, corner.R.M, double_corner_2, corner.R, platform, v_central],
        [platform.M, corner.R.M, double_corner_2, corner.R, platform, platform, v_central],
        [corner_gate.R.M, double_corner_2, corner.R, platform, platform, platform, v_central],
        [front_gate_extender_corner, corner_gate.R, platform, platform, platform, platform, v_end],
    ],
    remap=get_1cc_remap(CompanyColour.PURPLE),
)
