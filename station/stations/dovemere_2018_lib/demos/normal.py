from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()


normal_demo = Demo(
    "5×7 station layout (roughly 1 tile = 40m)",
    [
        [
            corner_platform.T,
            front_gate_platform.T,
            front_gate_extender_platform.T,
            front_gate_platform.TR,
            corner_platform.TR,
        ],
        [side_a_n.T, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.TR],
        [side_b_f.T, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.TR],
        [side_c, central_windowed, central_windowed_extender, central_windowed.R, side_c.R],
        [side_b_f, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.R],
        [side_a_n, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.R],
        [corner_platform, front_gate_platform, front_gate_extender_platform, front_gate_platform.R, corner_platform.R],
    ],
    remap=get_1cc_remap(CompanyColour.WHITE),
)
