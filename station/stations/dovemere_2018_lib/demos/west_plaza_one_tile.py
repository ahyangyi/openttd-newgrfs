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

station = h_merge([[[]] * 2, semitraversable.demo_1(1, 7)[5:], [[]] * 2], [[cns], [default]])

# Road Stops
west_stair_end = west_stair_end.lower_tile()
overpass = overpass.lower_tile()
roadstops = [[west_stair_end, overpass, west_stair_end.R]]

# Objects
center_ground = west_plaza_center.lower_tile()
flower = west_plaza_center_flower_2024_half.lower_tile()
west_square = [[center_ground, center_ground, center_ground], [center_ground, flower, center_ground]]


west_plaza_one_tile = Demo(
    "West plaza (extremely narrow station)",
    station + roadstops + west_square,
    remap=get_1cc_remap(CompanyColour.WHITE),
    merge_bbox=True,
)