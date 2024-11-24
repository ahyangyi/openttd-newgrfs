from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from .utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize()

# Road Stops
west_stair_end = west_stair_end.lower_tile()
overpass = overpass.lower_tile()
west_stair = west_stair_narrow.lower_tile()
west_stair_extender = west_stair_extender_narrow.lower_tile()

# Objects
center_ground = west_plaza_center.lower_tile()
offcenter_A = west_plaza_offcenter_A_decorated_lawn.lower_tile()
flower = west_plaza_center_flower_2024_half.lower_tile()
offcenter_B = west_plaza_offcenter_B_decorated.lower_tile()
edge = west_plaza_center_lawn.lower_tile()
edge_2 = west_plaza_center_toilet_lawn.lower_tile()
split_lawn = west_plaza_center_split_lawn.lower_tile()

station = [
    [None, overpass.M, front_gate_extender.M, None, front_gate_extender.T.M, overpass.T.M, None],
    [None, overpass.M, front_gate_extender_corner, front_gate_extender, front_gate_extender_corner.R, overpass.T.M, None],
    [west_stair_end, overpass, west_stair, west_stair_extender, west_stair.R, overpass, west_stair_end.R],
    [center_ground, edge, offcenter_A, center_ground, offcenter_A.R, edge, center_ground],
    [edge_2.T, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, edge_2.T.R],
    ]



west_plaza_three_sides = Demo(
    "West plaza (three sides)", station, remap=get_1cc_remap(CompanyColour.WHITE), merge_bbox=True
)
