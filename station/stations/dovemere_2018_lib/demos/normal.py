from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import roadstops
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from .utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
object_layouts.globalize()

station = h_merge(
    [[[]] * 7, semitraversable.demo_1(5, 7), [[]] * 7],
    [[concourse], [cns.T], [cns], [cns_d], [cns.T], [cns], [concourse.T]],
)

# Road Stops
stop1 = roadstops[0].doc_layout.lower_tile()
stop2 = roadstops[4].doc_layout.lower_tile()
stop3 = roadstops[12].doc_layout.lower_tile()
roadstops = [[stop1, stop1, stop2, stop3, stop2.R, stop1, stop1]]

# Objects
center_ground = west_plaza_center.lower_tile()
offcenter_ground = west_plaza_offcenter.lower_tile()
flower = west_plaza_center_flower_2024.lower_tile()
west_square = [
    [offcenter_ground] * 3 + [center_ground] + [offcenter_ground.M] * 3,
    [offcenter_ground] * 3 + [flower] + [offcenter_ground.M] * 3,
]


normal_demo = Demo(
    "5×7 station layout (roughly 1 tile = 40m)",
    station + roadstops + west_square,
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)
