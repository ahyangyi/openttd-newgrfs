from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    AParentSprite,
    ALayout,
    AChildSprite,
    AttrDict,
    Registers,
)
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from roadstop.lib import ARoadStop
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from ...misc import road_ground
from ..roadstop_utils import named_layouts, make_road_stop, register_road_stop, named_parts

cnt = 0
WIDTH = 3
TOTAL_HEIGHT = 12
OVERPASS_HEIGHT = 11
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 9

JOGGLE_AMOUNT = 45 - 32 * 2**0.5


def make_road_stops():
    make_road_stop(
        "overpass",
        BuildingSymmetricalX,
        0x8000,
        ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
        ((16, OVERHANG_WIDTH, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
        None,
        False,
        0,
        joggle=JOGGLE_AMOUNT,
    )

    overpass_far = named_parts[("overpass", "far")]
    overpass_overpass = named_parts[("overpass", "overpass")]
    layout = ALayout(
        road_ground,
        [overpass_far, overpass_overpass, overpass_far.T, overpass_overpass.T],
        True,
        category=b"\xe8\x8a\x9cR",
    )
    named_layouts[("double_overpass",)] = layout
    register_road_stop(layout, BuildingSymmetrical, 0x8002)
