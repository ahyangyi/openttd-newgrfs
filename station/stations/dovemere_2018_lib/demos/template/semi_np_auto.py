from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

row_4 = h_merge(
    [semitraversable.demo_2(i, 4) for i in range(1, 5)], [[concourse_none], [cns], [cns.T], [concourse_none]]
)
v_sep = [[concourse_none] * len(row_4[0])] * 2
row_5 = h_merge(
    [semitraversable.demo_2(i, 5) for i in range(1, 5)], [[concourse_none], [cns], [cns_d], [cns.T], [concourse_none]]
)
row_6 = h_merge(
    [semitraversable.demo_2(i, 6) for i in range(1, 5)],
    [[concourse_none], [cns], [cns.T], [cns], [cns.T], [concourse_none]],
)
row_7 = h_merge(
    [semitraversable.demo_2(i, 7) for i in range(1, 5)],
    [[concourse_none], [cns], [cns_d], [cns_d], [cns_d], [cns.T], [concourse_none]],
)

semi_np_auto_demo = Demo(
    row_4 + v_sep + row_5 + v_sep + row_6 + v_sep + row_7,
    "Semitraversable automatic stations (no platform)",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
