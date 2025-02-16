from station.lib import Demo
from ..realistic.normal import normal_demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from agrf.lib.building.layout import DefaultGraphics

for tile_id in [1011, 1012, 1313, 1314, 3981]:
    DefaultGraphics.register_third_party_image(f"third_party/cztr/{tile_id}.png", "cztr", tile_id)

cztr_demo = Demo(normal_demo.tiles, "with CZTR", remap=get_1cc_remap(CompanyColour.RED), climate="cztr")
