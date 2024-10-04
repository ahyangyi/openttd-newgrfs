from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import roadstops
from station.stations.dovemere_2018_lib.objects import objects
from station.stations.dovemere_2018_lib.layouts import globalize_all
from .utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

station = h_merge(
    [[[]] * 7, semitraversable.demo_1(5, 7), [[]] * 7],
    [[concourse], [cns.T], [cns], [cns_d], [cns.T], [cns], [concourse.T]],
)
stop1 = roadstops[0].doc_layout.lower_tile()
stop2 = roadstops[4].doc_layout.lower_tile()
stop3 = roadstops[12].doc_layout.lower_tile()
roadstops = [[stop1, stop1, stop2, stop3, stop2.R, stop1, stop1]]
square_ground = objects[0].doc_layout.lower_tile()
flower = objects[4].doc_layout.lower_tile()
west_square = [[square_ground] * 7, [square_ground] * 3 + [flower] + [square_ground] * 3]


normal_demo = Demo(
    "5×7 station layout (roughly 1 tile = 40m)",
    station + roadstops + west_square,
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)
