from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform, platform_s, platform_s
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

# FIXME
h_gate_1_third = h_gate
h_end_gate_third = h_end_gate
h_gate_extender_1_third = h_gate_extender

station_building = [
    tiny_third,
    platform_s.T,
    h_end_gate_third,
    h_end_gate_third.R,
    platform_s.T,
    h_end_gate_third,
    h_gate_extender_1_third,
    h_end_gate_third.R,
    platform_s.T,
    h_end_third,
    h_gate_1_third,
    h_gate_1_third.R,
    h_end_third.R,
]

side_third_auto_demo = Demo(
    "Traversable automatic stations",
    [[x.T for x in station_building], [platform_s.T] * 13, [platform_s] * 13, station_building],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
