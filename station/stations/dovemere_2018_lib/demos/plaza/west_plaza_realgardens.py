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
def real(x, y):
    return ALayout(AGroundSprite(image_sprite(f"third_party/realgardens/{x}.png", y=y)), [], True)


ground = real(315, 129).lower_tile()
crossroads = real(680, 129).lower_tile()
grassy = real(490, 185).lower_tile()
long_grassy = real(475, 143).lower_tile()
yard = real(576, 129).lower_tile()
path = real(560, 129).lower_tile()
pavilion_L = real(626, 157).lower_tile()
pavilion_R = real(624, 156).lower_tile()
tee_L = real(568, 208).lower_tile()
tee_R = real(570, 208).lower_tile()
big_tee = real(582, 188).lower_tile()
zig_L = real(648, 232).lower_tile()
zig_R = real(649, 197).lower_tile()
zag_L = real(647, 246).lower_tile()
zag_R = real(650, 240).lower_tile()
corner_L = real(640, 180).lower_tile()
corner_R = real(634, 253).lower_tile()
corner_TL = real(633, 240).lower_tile()
corner_TR = real(639, 253).lower_tile()
turn_L = real(585, 210).lower_tile()
turn_R = real(584, 241).lower_tile()


edge = real(615, 205).lower_tile()
edge_bottom = real(617, 241).lower_tile()


west_square = [
    [ground, grassy, ground, ground, ground, grassy, ground],
    [zag_L, edge_bottom, corner_TL, path, corner_TR, edge_bottom, zag_R],
    [corner_L, big_tee, zig_L, crossroads, zig_R, big_tee, corner_R],
    [pavilion_L, tee_L, grassy, path, grassy, tee_R, pavilion_R],
]


west_plaza_realgardens = Demo(
    station + roadstops + west_square,
    "West plaza (with RealGarden)",
    remap=get_1cc_remap(CompanyColour.GREEN),
    merge_bbox=True,
    climate="tropical",
)
