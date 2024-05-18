from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_s
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

special_demo_p = Demo(
    "Irregular 7×7 station layout",
    [
        [None, h_end_asym_gate.T, turn_gate.T.R, None, turn_gate.T, h_end_asym_gate.T.R, None],
        [platform_s, platform_s, v_central_n, platform_s, v_central_n, platform_s, platform_s],
        [platform_s.T, platform_s.T, v_central_n.T, platform_s.T, v_central_n.T, platform_s.T, platform_s.T],
        [
            h_end_corridor,
            h_windowed_corridor,
            cross,
            h_windowed_extender_corridor,
            cross,
            h_windowed_corridor.R,
            h_end_corridor.R,
        ],
        [platform_s, platform_s, v_central_n, platform_s, v_central_n, platform_s, platform_s],
        [platform_s.T, platform_s.T, v_central_n.T, platform_s.T, v_central_n.T, platform_s.T, platform_s.T],
        [None, h_end_asym_gate, turn_gate.R, None, turn_gate, h_end_asym_gate.R, None],
    ],
    remap=get_1cc_remap(CompanyColour.PALE_GREEN),
)
