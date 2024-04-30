from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_s, platform_s_nt
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()

station_building = [
    tiny_asym_platform,
    platform_s_nt.T,
    h_end_asym_gate_platform,
    h_end_asym_gate_platform.R,
    platform_s_nt.T,
    h_end_asym_gate_platform,
    h_gate_extender_1_platform,
    h_end_asym_gate_platform.R,
    platform_s_nt.T,
    h_end_asym_platform,
    h_gate_1_platform,
    h_gate_1_platform.R,
    h_end_asym_platform.R,
]

side_auto_demo = Demo(
    "Nontraversable automatic stations",
    [[x.T for x in station_building], [platform_s.T] * 13, [platform_s] * 13, station_building],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
