from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_d, platform_n, concourse_tile
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

platform_asym = platform_tiles.cns_side_and_shelter_1

row_2 = h_merge(
    [traversable.cb14.demo(i, 2, traversable.cb24_0) for i in range(1, 5)], [[platform_asym.T], [platform_asym]]
)
v_sep = [[concourse_tile] * len(row_2[0])] * 2
row_3 = h_merge(
    [traversable.cb14.demo(i, 3, traversable.cb24_0) for i in range(1, 5)],
    [[platform_asym.T], [platform_d], [platform_asym]],
)
row_4 = h_merge(
    [traversable.cb14.demo(i, 4, traversable.cb24_0) for i in range(1, 5)],
    [[platform_asym.T], [platform_n.T], [platform_n], [platform_asym]],
)
row_5 = h_merge(
    [traversable.cb14.demo(i, 5, traversable.cb24_0) for i in range(1, 5)],
    [[platform_asym.T], [platform_d], [platform_d], [platform_d], [platform_asym]],
)

full_auto_demo = Demo(
    "Fully traversable automatic stations",
    row_2 + v_sep + row_3 + v_sep + row_4 + v_sep + row_5,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
