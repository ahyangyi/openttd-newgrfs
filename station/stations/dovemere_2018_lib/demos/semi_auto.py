from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform, platform_s, platform_s_nt, gray_layout
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from .utils import h_merge

row_3 = h_merge(
    [semitraversable.cb14a.demo(i, 3, semitraversable.cb24_0) for i in range(1, 5)],
    [[platform_s_nt], [platform], [platform_s_nt.T]],
)
v_sep = [[gray_layout] * len(row_3[0])] * 2
row_4 = h_merge(
    [semitraversable.cb14a.demo(i, 4, semitraversable.cb24_0) for i in range(1, 5)],
    [[platform_s_nt], [platform_s.T], [platform_s], [platform_s_nt.T]],
)
row_5 = h_merge(
    [semitraversable.cb14a.demo(i, 5, semitraversable.cb24_0) for i in range(1, 5)],
    [[platform_s_nt], [platform], [platform], [platform], [platform_s_nt.T]],
)
row_6 = h_merge(
    [semitraversable.cb14a.demo(i, 6, semitraversable.cb24_0) for i in range(1, 5)],
    [[platform_s_nt], [platform_s.T], [platform_s], [platform_s.T], [platform_s], [platform_s_nt.T]],
)

semi_auto_demo = Demo(
    "Semitraversable automatic stations",
    row_3 + v_sep + row_4 + v_sep + row_5 + v_sep + row_6,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
