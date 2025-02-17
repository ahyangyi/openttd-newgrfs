import grf
from station.lib import Demo, AGroundSprite, ALayout
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.image_sprite import image_sprite
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
stair_end = stair_end.lower_tile()
overpass = overpass.lower_tile()
stair = stair_narrow.lower_tile()
stair_extender = stair_extender_narrow.lower_tile()
roadstops = [[stair_end, overpass, stair, stair_extender, stair.R, overpass, stair_end.R]]


# Objects
def real(x, y):
    return ALayout(AGroundSprite(image_sprite(f"third_party/realgardens/{x}.png", y=y)), [], True)


ground = real(315, 129).lower_tile()
crossroads = real(680, 129).lower_tile()
grassy = real(490, 185).lower_tile()
yard = real(576, 129).lower_tile()
west_square = [
    [ground, ground, ground, yard, ground, ground, ground],
    [ground, ground, ground, crossroads, ground, ground, ground],
    [ground, grassy, ground, ground, ground, grassy, ground],
]


west_plaza_realgardens = Demo(
    station + roadstops + west_square,
    "West plaza (with RealGarden)",
    remap=get_1cc_remap(CompanyColour.MAUVE),
    merge_bbox=True,
)
