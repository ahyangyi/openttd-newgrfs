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
    gs = named_grounds[("west_plaza_offcenter_A", "")]
    ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "decorated")] = layout
    register([[layout]], BuildingFull, b"L")


def make_mixed_objects():
    gs = named_grounds[("west_plaza_offcenter_B", "")]
    ps = [
        planter_1.move(-4, 0),
        planter_2,
        pole.move(-2, 0),
        pole.move(2, 0),
        pole.move(-2, -4),
        pole.move(2, -4),
        underground_entrance.move(6, -6),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_B", "decorated")] = layout
    register([[layout]], BuildingFull, b"M")

    gs = named_grounds[("west_plaza_offcenter_A", "")]
    ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8), corner_lawn]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_A", "decorated_lawn")] = layout
    register([[layout]], BuildingFull, b"M")

    gs = named_grounds[("west_plaza_offcenter_A", "")]
    ps = [pole.move(-2, 0), pole.move(2, 0), pole.move(-2, 4), pole.move(2, 4), underground_entrance.move(6, 2)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_offcenter_B", "oneliner")] = layout
    register([[layout]], BuildingFull, b"M")

    gs = named_grounds[("west_plaza_center", "")]
    ps = [
        edge_lawn,
        tree_bush.R.M.move(-3, 5),
        tree_bench.M.move(0, 5),
        tree_bush.T.R.move(3, 5),
        tree_bench.R.move(-3, 7),
        tree_bush.move(0, 7),
        tree_bench.T.R.M.move(3, 7),
        glass_pyramid.move(-5, 6),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "lawn")] = layout
    register([[layout]], BuildingFull, b"M")

    gs = named_grounds[("west_plaza_center", "")]
    ps = [edge_lawn, underground_entrance.move(0, 6)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "toilet_lawn")] = layout
    register([[layout]], BuildingSymmetricalX, b"M")

    gs = named_grounds[("west_plaza_center", "")]
    ps = [
        split_lawn,
        tree_bench.R.M.move(-3, -5),
        tree_bush.M.move(0, -5),
        tree_bench.T.R.move(3, -5),
        tree_bush.R.move(-3, -7),
        tree_bench.move(0, -7),
        tree_bush.T.R.M.move(3, -7),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[("west_plaza_center", "split_lawn")] = layout
    register([[layout]], BuildingFull, b"M")


def make_objects():
    components.globalize()
    make_lightposts()
    make_mixed_objects()
