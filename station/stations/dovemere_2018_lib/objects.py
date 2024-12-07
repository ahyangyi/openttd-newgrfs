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
from .west_plaza.grounds import named_grounds, make_ground_layouts
from .west_plaza.topiary import make_topiaries
from .objects_utils import objects, register_slopes, DEFAULT_FLAGS, named_layouts, register

make_ground_layouts()
make_topiaries()


def object_part(name, sym, span, offset, has_nosnow=False):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )

    bare = v.discard_layers(("snow", "nosnow"), "bare")
    bare.config["agrf_manual_crop"] = (0, 11)
    bare.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(
        bare.spritesheet(xspan=span[1], yspan=span[0], xdiff=offset[1], ydiff=offset[0], zdiff=offset[2])
    )

    snow = v.keep_layers(("snow",), "snow")
    snow = snow.compose(bare, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    snow.config["agrf_childsprite"] = (0, -11)
    snow.in_place_subset(sym.render_indices())
    snowsprite = sym.create_variants(snow.spritesheet())
    snowcs = AChildSprite(snowsprite, (0, 0), flags={"dodraw": Registers.SNOW})

    gs = AParentSprite(sprite, span, offset) + snowcs

    if has_nosnow:
        nosnow = v.keep_layers(("nosnow",), "no_snow")
        nosnow = nosnow.compose(bare, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
        nosnow.config["agrf_childsprite"] = (0, -11)
        nosnow.in_place_subset(sym.render_indices())
        nosnowsprite = sym.create_variants(nosnow.spritesheet())
        nosnowcs = AChildSprite(nosnowsprite, (0, 0), flags={"dodraw": Registers.NOSNOW})
        gs = gs + nosnowcs

    return gs


planter_1 = object_part("west_plaza_planter_1", BuildingFull, (4, 4, 1), (2, 10, 0)).move(-4, 0)
planter_2 = object_part("west_plaza_planter_2", BuildingFull, (7, 4, 1), (2, 10, 0))
pole = object_part("west_plaza_pole", BuildingCylindrical, (2, 2, 8), (7, 7, 0))
underground_entrance = object_part("west_plaza_underground_entrance", BuildingFull, (4, 4, 8), (6, 6, 0))
corner_lawn = object_part("corner_lawn", BuildingDiagonalAlt, (6, 6, 1), (10, 0, 0))
edge_lawn = object_part("edge_lawn", BuildingSymmetricalX, (16, 6, 1), (0, 0, 0))
split_lawn = object_part("split_lawn", BuildingFull, (16, 6, 1), (0, 10, 0))
tree_bench = object_part("west_plaza_tree_bench", BuildingFull, (2, 2, 8), (7, 7, 0), has_nosnow=True)
tree_bush = object_part("west_plaza_tree_bush", BuildingFull, (2, 2, 8), (7, 7, 0), has_nosnow=True)
glass_pyramid = object_part("west_plaza_glass_pyramid", BuildingSymmetrical, (2, 2, 8), (7, 7, 0))

gs = named_grounds[("west_plaza_offcenter_B", "")]
ps = [
    planter_1,
    planter_2,
    pole.move(-2, 0),
    pole.move(2, 0),
    pole.move(-2, -4),
    pole.move(2, -4),
    underground_entrance.move(6, -6),
]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_B", "decorated")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8)]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_A", "decorated")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8), corner_lawn]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_A", "decorated_lawn")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 0), pole.move(2, 0), pole.move(-2, 4), pole.move(2, 4), underground_entrance.move(6, 2)]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_B", "oneliner")] = layout
register([[layout]], BuildingFull, b"L")

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
register([[layout]], BuildingSymmetricalX, b"l")

gs = named_grounds[("west_plaza_center", "")]
ps = [edge_lawn, underground_entrance.move(0, 6)]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_center", "toilet_lawn")] = layout
register([[layout]], BuildingSymmetricalX, b"l")

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
register([[layout]], BuildingSymmetricalX, b"l")
