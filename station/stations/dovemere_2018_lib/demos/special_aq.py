from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *

special_demo_aq = Demo(
    "Irregular 7×7 station layout",
    [
        [None, platform.M, platform.M, platform.M, platform.M, platform.M, None],
        [
            corner_gate.R.M,
            side_a3_windowed.R.M,
            side_a3_windowed.TR.M,
            side_a3_windowed.R.M,
            side_a3_windowed.TR.M,
            side_a2_windowed.R.M,
            corner_gate.TR.M,
        ],
        [
            corner_gate.M,
            side_a2_windowed.T.M,
            side_a3_windowed.M,
            side_a3_windowed.T.M,
            side_a3_windowed.M,
            side_a3_windowed.T.M,
            corner_gate.T.M,
        ],
        [None, platform.M, platform.M, platform.M, platform.M, platform.M, None],
        [
            corner_gate.R.M,
            side_a3_windowed.R.M,
            side_a3_windowed.TR.M,
            side_a3_windowed.R.M,
            side_a3_windowed.TR.M,
            side_a2_windowed.R.M,
            corner_gate.TR.M,
        ],
        [
            corner_gate.M,
            side_a2_windowed.T.M,
            side_a3_windowed.M,
            side_a3_windowed.T.M,
            side_a3_windowed.M,
            side_a3_windowed.T.M,
            corner_gate.T.M,
        ],
        [None, platform.M, platform.M, platform.M, platform.M, platform.M, None],
    ],
)
