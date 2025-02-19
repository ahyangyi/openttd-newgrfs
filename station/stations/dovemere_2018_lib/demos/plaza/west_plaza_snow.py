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
    [[[cns], [slope_2.lower_tile()]], semitraversable.demo_1(5, 7)[5:], [[cns], [slope_2.lower_tile()]]], [[], []]
)

# Road Stops
stair_end = stair_end.lower_tile()
overpass = overpass.lower_tile()
stair = stair_narrow.lower_tile()
stair_extender = stair_extender_narrow.lower_tile()
roadstops = [[stair_end, overpass, stair, stair_extender, stair.R, overpass, stair_end.R]]

# Objects
center_ground = west_plaza_center.lower_tile()
offcenter_A = west_plaza_offcenter_A_decorated_lawn.lower_tile()
flower = west_plaza_topiary_2024a_half.lower_tile()
offcenter_B = west_plaza_offcenter_B_decorated.lower_tile()
edge = west_plaza_center_lawn.lower_tile()
edge_2 = west_plaza_center_toilet_lawn.lower_tile()
split_lawn = west_plaza_center_split_lawn.lower_tile()
west_square = [
    [center_ground, edge, offcenter_A, center_ground, offcenter_A.R, edge.R, center_ground],
    [edge_2.T, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, edge_2.T.R],
]


west_plaza_snow = Demo(
    station + roadstops + west_square,
    "West plaza (snow)",
    remap=get_1cc_remap(CompanyColour.PINK),
    merge_bbox=True,
    climate="arctic",
    subclimate="snow",
)
