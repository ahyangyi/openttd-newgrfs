from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *

special_demo_p = Demo(
    "Irregular 7×7 station layout",
    [
        [None, h_end_gate_1.T, turn_gate.TR, None, turn_gate.T, h_end_gate_1.TR, None],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [h_end, h_windowed, junction4, h_windowed_extender, junction4, h_windowed.R, h_end.R],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [platform, platform, v_central, platform, v_central, platform, platform],
        [None, h_end_gate_1, turn_gate.R, None, turn_gate, h_end_gate_1.R, None],
    ],
)