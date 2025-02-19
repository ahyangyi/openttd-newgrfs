from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import slope_2
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize()

station = h_merge(
    [[[cns], [slope_2.lower_tile()]], semitraversable.demo_1(4, 6)[4:], [[cns], [slope_2.lower_tile()]]], [[], []]
)

# Road Stops
stair_end = stair_end.lower_tile()
overpass = overpass.lower_tile()
stair = stair_wide.lower_tile()
roadstops = [[stair_end, overpass, stair, stair.R, overpass, stair_end.R]]

# Objects
center_ground = west_plaza_center.lower_tile()
offcenter_A = west_plaza_offcenter_A_decorated.lower_tile()
flower = west_plaza_topiary_2024a_half_horizontal.lower_tile()
offcenter_B = west_plaza_offcenter_B_decorated.lower_tile()
split_lawn = west_plaza_center_split_lawn.lower_tile()
west_square = [
    [center_ground, offcenter_A, center_ground, center_ground, offcenter_A.R, center_ground],
    [split_lawn, offcenter_B, flower, center_ground, offcenter_B.R, split_lawn.R],
]


west_plaza_4 = Demo(
    station + roadstops + west_square,
    "West plaza (4 tiles version)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)
