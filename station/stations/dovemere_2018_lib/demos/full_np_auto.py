from station.lib import Demo
from station.stations.platforms import platform_tiles, concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

platform_tiles.globalize()

row_1 = h_merge([traversable.demo_2(i, 1) for i in range(1, 5)], [[cns_shelter_2_d]])
v_sep = [[concourse] * len(row_1[0])] * 2
row_2 = h_merge([traversable.demo_2(i, 2) for i in range(1, 5)], [[cns_shelter_2.T], [cns_shelter_2]])
row_4 = h_merge(
    [traversable.demo_2(i, 4) for i in range(1, 5)],
    [[cns_shelter_2.T], [cns_shelter_2], [cns_shelter_2.T], [cns_shelter_2]],
)
row_5 = h_merge(
    [traversable.demo_2(i, 5) for i in range(1, 5)],
    [[cns_shelter_2.T], [cns_shelter_2], [cns_shelter_2_d], [cns_shelter_2.T], [cns_shelter_2]],
)

full_np_auto_demo = Demo(
    "Fully traversable automatic stations (no platform at ends)",
    row_1 + v_sep + row_2 + v_sep + row_4 + v_sep + row_5,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
