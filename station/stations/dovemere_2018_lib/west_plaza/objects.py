from agrf.graphics.voxel import LazyVoxel
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    BuildingCylindrical,
    BuildingDiamond,
    BuildingDiagonalAlt,
    BuildingRotational4,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
    Registers,
    Demo,
)
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from .grounds import named_grounds, make_ground_layouts
from .topiary import make_topiaries
from .components import make_components, components
from ..objects_utils import objects, register_slopes, DEFAULT_FLAGS, named_layouts, register


def make_lightposts():
    pass


def make_mixed_objects():
    pass


def make_objects():
    components.globalize()
    make_lightposts()
    make_mixed_objects()
