from station.lib import Demo
from station.stations.platforms import cns_shelter_2, cns_shelter_2_d, concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from .utils import h_merge

row_4 = h_merge(
    [semitraversable.demo_2(i, 4) for i in range(1, 5)], [[concourse], [cns_shelter_2], [cns_shelter_2.T], [concourse]]
)
v_sep = [[concourse] * len(row_4[0])] * 2
row_5 = h_merge(
    [semitraversable.demo_2(i, 5) for i in range(1, 5)],
    [[concourse], [cns_shelter_2], [cns_shelter_2_d], [cns_shelter_2.T], [concourse]],
)
row_6 = h_merge(
    [semitraversable.demo_2(i, 6) for i in range(1, 5)],
    [[concourse], [cns_shelter_2], [cns_shelter_2.T], [cns_shelter_2], [cns_shelter_2.T], [concourse]],
)
row_7 = h_merge(
    [semitraversable.demo_2(i, 7) for i in range(1, 5)],
    [
        [concourse],
        [cns_shelter_2],
        [cns_shelter_2_d],
        [cns_shelter_2_d],
        [cns_shelter_2_d],
        [cns_shelter_2.T],
        [concourse],
    ],
)

semi_np_auto_demo = Demo(
    "Semitraversable automatic stations (no platform)",
    row_4 + v_sep + row_5 + v_sep + row_6 + v_sep + row_7,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
