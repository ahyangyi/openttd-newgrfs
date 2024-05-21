from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_d, platform_n, concourse_tile
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from .utils import h_merge

nt = platform_tiles.concourse_side_shelter

row_3 = h_merge(
    [semitraversable.cb14a.demo(i, 3, semitraversable.cb24_0) for i in range(1, 5)], [[nt], [platform_d], [nt.T]]
)
v_sep = [[concourse_tile] * len(row_3[0])] * 2
row_4 = h_merge(
    [semitraversable.cb14a.demo(i, 4, semitraversable.cb24_0) for i in range(1, 5)],
    [[nt], [platform_n.T], [platform_n], [nt.T]],
)
row_5 = h_merge(
    [semitraversable.cb14a.demo(i, 5, semitraversable.cb24_0) for i in range(1, 5)],
    [[nt], [platform_d], [platform_d], [platform_d], [nt.T]],
)
row_6 = h_merge(
    [semitraversable.cb14a.demo(i, 6, semitraversable.cb24_0) for i in range(1, 5)],
    [[nt], [platform_n.T], [platform_n], [platform_n.T], [platform_n], [nt.T]],
)

semi_auto_demo = Demo(
    "Semitraversable automatic stations",
    row_3 + v_sep + row_4 + v_sep + row_5 + v_sep + row_6,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
