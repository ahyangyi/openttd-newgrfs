from station.lib import Demo, AGroundSprite, ALayout
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.image_sprite import image_sprite
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
def vast(x):
    return ALayout(AGroundSprite(image_sprite(f"third_party/vast/vast_{x}.png")), [], True)


ground = vast(26).lower_tile()
symbol = vast(47).lower_tile()
grassy = vast(70).lower_tile()
west_square = [
    [ground, grassy, ground, ground, ground, grassy, ground],
    [grassy, grassy, ground, symbol, ground, grassy, grassy],
    [grassy, ground, ground, ground, ground, ground, grassy],
]


west_plaza_vast = Demo(
    station + roadstops + west_square,
    "West plaza (with VAST Objects tiles)",
    remap=get_1cc_remap(CompanyColour.MAUVE),
    merge_bbox=True,
)
