from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform, platform_s, gray_layout, rail
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

row_1 = h_merge([traversable.cb14.demo(i, 1, traversable.cb24_1) for i in range(1, 5)], [[rail]])
v_sep = [[gray_layout] * len(row_1[0])] * 2
row_2 = h_merge([traversable.cb14.demo(i, 2, traversable.cb24_1) for i in range(1, 5)], [[rail], [rail]])
row_4 = h_merge(
    [traversable.cb14.demo(i, 4, traversable.cb24_1) for i in range(1, 5)],
    [[rail], [platform_s], [platform_s.T], [rail]],
)
row_5 = h_merge(
    [traversable.cb14.demo(i, 5, traversable.cb24_1) for i in range(1, 5)],
    [[rail], [platform_s], [platform], [platform_s.T], [rail]],
)

full_np_auto_demo = Demo(
    "Fully traversable automatic stations (no platform at ends)",
    row_1 + v_sep + row_2 + v_sep + row_4 + v_sep + row_5,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
