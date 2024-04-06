from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *

special_demo_g = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end, junction3.T, h_windowed, h_windowed_extender, h_windowed.R, junction3.T, h_end.R],
        [platform, v_central, platform, platform, platform, v_central, platform],
        [platform, v_central, platform, platform, platform, v_central, platform],
        [platform, v_central, platform, platform, platform, v_central, platform],
        [platform, v_central, platform, platform, platform, v_central, platform],
        [platform, v_central, platform, platform, platform, v_central, platform],
        [h_end, junction3, h_gate, h_gate_extender, h_gate.R, junction3, h_end.R],
    ],
)
