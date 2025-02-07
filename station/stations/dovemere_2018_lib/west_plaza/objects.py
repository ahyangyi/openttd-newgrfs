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
    gs = named_grounds[("offcenter_A", "")]
    ps = [object_pole.move(-2, 4), object_pole.move(2, 4), object_pole.move(-2, 8), object_pole.move(2, 8)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "decorated")] = layout
    register([[layout]], BuildingFull, b"L", starting_id=0x0200)


def make_lawns():
    gs = named_grounds[("offcenter_A", "")]
    ps = [lawn_corner]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "corner_lawn")] = layout
    register([[layout]], BuildingFull, b"l", starting_id=0x0300)

    gs = named_grounds[("offcenter_A", "")]
    ps = [lawn_corner_2]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "corner_lawn_2")] = layout
    register([[layout]], BuildingFull, b"l", starting_id=0x0302)


def make_mixed_objects():
    gs = named_grounds[("offcenter_B", "")]
    ps = [
        planter_1.move(-4, 0),
        planter_2,
        object_pole.move(-2, 0),
        object_pole.move(2, 0),
        object_pole.move(-2, -4),
        object_pole.move(2, -4),
        object_underground_entrance.move(6, -6),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_B", "decorated")] = layout
    register([[layout]], BuildingFull, b"M", starting_id=0x0700)

    gs = named_grounds[("offcenter_A", "")]
    ps = [object_pole.move(-2, 4), object_pole.move(2, 4), object_pole.move(-2, 8), object_pole.move(2, 8), lawn_corner]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "decorated_lawn")] = layout
    register([[layout]], BuildingFull, b"M", starting_id=0x0702)

    gs = named_grounds[("offcenter_A", "")]
    ps = [
        object_pole.move(-2, 0),
        object_pole.move(2, 0),
        object_pole.move(-2, 4),
        object_pole.move(2, 4),
        object_underground_entrance.move(6, 2),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_B", "oneliner")] = layout
    register([[layout]], BuildingFull, b"M", starting_id=0x0704)

    gs = named_grounds[("center", "")]
    ps = [
        lawn_edge,
        tree_bush.R.M.move(-3, 5),
        tree_bench.M.move(0, 5),
        tree_bush.T.R.move(3, 5),
        tree_bench.R.move(-3, 7),
        tree_bush.move(0, 7),
        tree_bench.T.R.M.move(3, 7),
        object_glass_pyramid.move(-5, 6),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "lawn")] = layout
    register([[layout]], BuildingFull, b"M", starting_id=0x0706)

    gs = named_grounds[("center", "")]
    ps = [lawn_edge, object_underground_entrance.move(0, 6)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "toilet_lawn")] = layout
    register([[layout]], BuildingSymmetricalX, b"M", starting_id=0x0708)

    gs = named_grounds[("center", "")]
    ps = [
        lawn_split,
        tree_bench.R.M.move(-3, -5),
        tree_bush.M.move(0, -5),
        tree_bench.T.R.move(3, -5),
        tree_bush.R.move(-3, -7),
        tree_bench.move(0, -7),
        tree_bush.T.R.M.move(3, -7),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "split_lawn")] = layout
    register([[layout]], BuildingFull, b"M", starting_id=0x070A)


def make_objects():
    components.globalize()
    make_lightposts()
    make_lawns()
    make_mixed_objects()
