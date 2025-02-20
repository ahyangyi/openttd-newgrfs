from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.layouts import globalize_all, concourse_tiles
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

row_1 = h_merge([traversable.demo_2(i, 1) for i in range(1, 5)], [[cns_d]])
v_sep = [[concourse_tiles.none] * len(row_1[0])] * 2
row_2 = h_merge([traversable.demo_2(i, 2) for i in range(1, 5)], [[cns.T], [cns]])
row_4 = h_merge([traversable.demo_2(i, 4) for i in range(1, 5)], [[cns.T], [cns], [cns.T], [cns]])
row_5 = h_merge([traversable.demo_2(i, 5) for i in range(1, 5)], [[cns.T], [cns], [cns_d], [cns.T], [cns]])

full_np_auto_demo = Demo(
    row_1 + v_sep + row_2 + v_sep + row_4 + v_sep + row_5,
    "Fully traversable automatic stations (no platform at ends)",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
