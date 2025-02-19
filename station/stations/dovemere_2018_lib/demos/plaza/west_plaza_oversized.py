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
    [[[cns], [slope_2.lower_tile()]], semitraversable.demo_1(14, 22)[20:], [[cns], [slope_2.lower_tile()]]], [[], []]
)

# Road Stops
stair_end = stair_end.lower_tile()
overpass = overpass.lower_tile()
stair = stair.lower_tile()
stair_extender = stair_extender.lower_tile()
roadstops = [[stair_end] + [overpass] * 4 + [stair] + [stair_extender] * 4 + [stair.R] + [overpass] * 4 + [stair_end.R]]

# Objects
center_ground = west_plaza_center.lower_tile()
offcenter_A = west_plaza_offcenter_A_decorated.lower_tile()
lightposts = west_plaza_offcenter_A_lightposts.lower_tile()
flower = west_plaza_topiary_2024a_corner.lower_tile()
offcenter_B = west_plaza_offcenter_B_decorated.lower_tile()
trees = west_plaza_center_tree_formation.lower_tile()
split_lawn = west_plaza_center_split_lawn.lower_tile()
west_square = [
    [center_ground] * 5
    + [offcenter_A, center_ground, center_ground, center_ground, center_ground, offcenter_A.R]
    + [center_ground] * 5,
    [center_ground] * 4
    + [trees, lightposts, center_ground, center_ground, center_ground, center_ground, lightposts.R, trees]
    + [center_ground] * 4,
    [center_ground] * 4
    + [trees, lightposts, center_ground, flower, center_ground, center_ground, lightposts.R, trees]
    + [center_ground] * 4,
    [center_ground] * 4
    + [split_lawn, offcenter_B, center_ground, center_ground, center_ground, center_ground, offcenter_B.R, split_lawn.R]
    + [center_ground] * 4,
]


west_plaza_oversized = Demo(
    station + roadstops + west_square,
    "West plaza (oversized version)",
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)
