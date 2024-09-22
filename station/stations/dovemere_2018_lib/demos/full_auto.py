from station.lib import Demo
from station.stations.platforms import platform_tiles, two_side_tiles, concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

platform_asym = two_side_tiles.cns_concrete_concrete_shelter_2
platform_tiles.globalize()

row_2 = h_merge([traversable.demo_1(i, 2) for i in range(1, 5)], [[platform_asym.T], [platform_asym]])
v_sep = [[concourse] * len(row_2[0])] * 2
row_3 = h_merge(
    [traversable.demo_1(i, 3) for i in range(1, 5)], [[platform_asym.T], [cns_shelter_2_d], [platform_asym]]
)
row_4 = h_merge(
    [traversable.demo_1(i, 4) for i in range(1, 5)],
    [[platform_asym.T], [cns_shelter_2.T], [cns_shelter_2], [platform_asym]],
)
row_5 = h_merge(
    [traversable.demo_1(i, 5) for i in range(1, 5)],
    [[platform_asym.T], [cns_shelter_2_d], [cns_shelter_2_d], [cns_shelter_2_d], [platform_asym]],
)

full_auto_demo = Demo(
    "Fully traversable automatic stations",
    row_2 + v_sep + row_3 + v_sep + row_4 + v_sep + row_5,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
