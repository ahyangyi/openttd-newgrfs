from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import named_layouts as roadstop_layouts
from station.stations.dovemere_2018_lib.objects import named_layouts as object_layouts
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.stations.misc import default
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")
roadstop_layouts.globalize()
object_layouts.globalize()

station = h_merge([[[]] * 2, semitraversable.demo_1(5, 7)[5:], [[]] * 2], [[cns], [default]])

# Road Stops
overpass = overpass.lower_tile()
roadstops = [[None] + [overpass] * 5 + [None]]

# Objects
center_ground = east_plaza_center.lower_tile()
east_square = [[center_ground] * 7] * 2

east_plaza = Demo(
    station + roadstops + east_square, "West plaza", remap=get_1cc_remap(CompanyColour.WHITE), merge_bbox=True
)
