from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.layouts import globalize_all, concourse_tiles
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

row_2 = h_merge([traversable.demo_1(i, 2) for i in range(1, 5)], [[cns_side_and.T], [cns_side_and]])
v_sep = [[concourse_tiles.none] * len(row_2[0])] * 2
row_3 = h_merge([traversable.demo_1(i, 3) for i in range(1, 5)], [[cns_side_and.T], [cns_d], [cns_side_and]])
row_4 = h_merge([traversable.demo_1(i, 4) for i in range(1, 5)], [[cns_side_and.T], [cns.T], [cns], [cns_side_and]])
row_5 = h_merge(
    [traversable.demo_1(i, 5) for i in range(1, 5)], [[cns_side_and.T], [cns_d], [cns_d], [cns_d], [cns_side_and]]
)

full_auto_demo = Demo(
    row_2 + v_sep + row_3 + v_sep + row_4 + v_sep + row_5,
    "Fully traversable automatic stations",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
