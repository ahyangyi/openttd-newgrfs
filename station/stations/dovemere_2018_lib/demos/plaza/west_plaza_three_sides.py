from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import road_ground_turn_layout

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize()

# Road Stops
stair_end = stair_end.lower_tile()
overpass = overpass.lower_tile()
stair = stair_narrow.lower_tile()
stair_extender = stair_extender_narrow.lower_tile()

# Objects
diagonal = west_plaza_diagonal.lower_tile()
center_ground = west_plaza_center.lower_tile()
offcenter_A = west_plaza_offcenter_A_corner_lawn_2.lower_tile()
flower = west_plaza_topiary_2024a_half.lower_tile()
offcenter_B = west_plaza_offcenter_B_decorated.lower_tile()
edge = west_plaza_center_lawn.lower_tile()
edge_2 = west_plaza_center_toilet_lawn.lower_tile()
split_lawn = west_plaza_center_split_lawn.lower_tile()

station = [
    [
        center_ground.M,
        edge.M,
        overpass.M,
        front_gate_extender.M,
        None,
        front_gate_extender.T.M,
        overpass.T.M,
        edge.T.M,
        center_ground.T.M,
    ],
    [
        center_ground.M,
        edge.M,
        overpass.M,
        front_gate_extender_corner,
        front_gate_extender,
        front_gate_extender_corner.R,
        overpass.T.M,
        edge.T.M,
        center_ground.T.M,
    ],
    [
        center_ground.M,
        edge.M,
        road_ground_turn_layout.lower_tile(),
        stair,
        stair_extender,
        stair.R,
        road_ground_turn_layout.R.lower_tile(),
        edge.T.M,
        center_ground.T.M,
    ],
    [
        diagonal.M,
        offcenter_A.R.M,
        edge,
        offcenter_A,
        center_ground,
        offcenter_A.R,
        edge.R,
        offcenter_A.T.R.M,
        diagonal.T.M,
    ],
    [diagonal.M, diagonal.M, split_lawn, offcenter_B, flower, offcenter_B.R, split_lawn.R, diagonal.T.M, diagonal.T.M],
]


west_plaza_three_sides = Demo(
    station, "West plaza (three sides)", remap=get_1cc_remap(CompanyColour.WHITE), merge_bbox=True
)
