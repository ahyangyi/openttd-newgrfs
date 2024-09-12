from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import concourse_tile
from station.stations.platforms import named_tiles as platform_tiles, cns_shelter_2, cns_shelter_2_d
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from .utils import h_merge

nt = platform_tiles.concourse_side_shelter_2

row_3 = h_merge([semitraversable.demo_1(i, 3) for i in range(1, 5)], [[nt], [cns_shelter_2_d], [nt.T]])
v_sep = [[concourse_tile] * len(row_3[0])] * 2
row_4 = h_merge([semitraversable.demo_1(i, 4) for i in range(1, 5)], [[nt], [cns_shelter_2.T], [cns_shelter_2], [nt.T]])
row_5 = h_merge(
    [semitraversable.demo_1(i, 5) for i in range(1, 5)],
    [[nt], [cns_shelter_2_d], [cns_shelter_2_d], [cns_shelter_2_d], [nt.T]],
)
row_6 = h_merge(
    [semitraversable.demo_1(i, 6) for i in range(1, 5)],
    [[nt], [cns_shelter_2.T], [cns_shelter_2], [cns_shelter_2.T], [cns_shelter_2], [nt.T]],
)

semi_auto_demo = Demo(
    "Semitraversable automatic stations",
    row_3 + v_sep + row_4 + v_sep + row_5 + v_sep + row_6,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
