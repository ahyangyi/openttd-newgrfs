from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_d, platform_n, concourse_tile
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

row_1 = h_merge([traversable.demo_2(i, 1) for i in range(1, 5)], [[platform_d]])
v_sep = [[concourse_tile] * len(row_1[0])] * 2
row_2 = h_merge([traversable.demo_2(i, 2) for i in range(1, 5)], [[platform_n.T], [platform_n]])
row_4 = h_merge(
    [traversable.demo_2(i, 4) for i in range(1, 5)], [[platform_n.T], [platform_n], [platform_n.T], [platform_n]]
)
row_5 = h_merge(
    [traversable.demo_2(i, 5) for i in range(1, 5)],
    [[platform_n.T], [platform_n], [platform_d], [platform_n.T], [platform_n]],
)

full_np_auto_demo = Demo(
    "Fully traversable automatic stations (no platform at ends)",
    row_1 + v_sep + row_2 + v_sep + row_4 + v_sep + row_5,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
