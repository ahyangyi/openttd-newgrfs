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
from ..objects_utils import objects, register_slopes, DEFAULT_FLAGS, named_layouts, register


def make_object_layout(name, sym, Xspan, Yspan, xspan, yspan, height, osym=None):
    if osym is None:
        osym = sym

    gs = named_grounds[("west_plaza_center", "")]
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    snow = v.keep_layers(("snow",), "snow")
    snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    snow.config["agrf_childsprite"] = (0, -11)
    snow.in_place_subset(osym.render_indices())
    snowsprite = osym.create_variants(snow.spritesheet())

    ground_snow = v.keep_layers(("ground snow",), "ground_snow")
    ground_snow = ground_snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    ground_snow.config["agrf_childsprite"] = (0, -10)
    ground_snow.in_place_subset(sym.render_indices())
    ground_snowsprite = sym.create_variants(ground_snow.spritesheet())

    v = v.discard_layers(("snow", "ground snow"), "nosnow")
    ground = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_ground_mask.vox", "ground")
    ground.config["agrf_manual_crop"] = (0, 10)
    ground.in_place_subset(sym.render_indices())
    groundsprite = sym.create_variants(ground.spritesheet())

    gscs = AChildSprite(groundsprite, (0, 0))
    ground_snowcs = AChildSprite(ground_snowsprite, (0, 0), flags={"dodraw": Registers.SNOW})
    gs2 = gs + gscs + ground_snowcs

    xofs = (16 - xspan) // 2
    yofs = (16 - yspan) // 2
    Xofs = (16 - Xspan) // 2
    Yofs = (16 - Yspan) // 2

    v = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_mask.vox", "object")
    v.config["agrf_manual_crop"] = (0, 11)
    v.in_place_subset(osym.render_indices())
    sprite = osym.create_variants(v.spritesheet(xdiff=xofs, xspan=xspan, ydiff=yofs, yspan=yspan, zdiff=1))
    snowcs = AChildSprite(snowsprite, (0, 0), flags={"dodraw": Registers.SNOW})

    # ps = [AParentSprite(sprite, (yspan, xspan, height), (yofs, xofs, 0)) + snowcs]
    # layout = ALayout(gs2, ps, True, category=b"\xe8\x8a\x9cZ")
    # named_layouts[(name, "grounded")] = layout
    # register(layout, sym, b'F')

    gl = named_layouts[("west_plaza_center", "")]

    groundsprite2 = sym.create_variants(ground.spritesheet(xdiff=Xofs, xspan=Xspan, ydiff=Yofs, yspan=Yspan))
    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "")] = layout
    register([[layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs - 4, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs - 4, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "half")] = layout
    register([[layout]], sym.break_y_symmetry(), b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs - 8, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs - 8, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "vertical")] = layout
    register([[gl], [layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "horizontal")] = layout
    register([[gl, layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs - 4, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs - 4, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "half_horizontal")] = layout
    register([[gl, layout]], sym.break_y_symmetry(), b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs - 8, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs - 8, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "corner")] = layout
    register([[gl, gl], [gl, layout]], sym, b"F")


def make_topiaries():
    make_object_layout("west_plaza_topiary_2021", BuildingSymmetrical, 8, 10, 4, 8, 6)
    make_object_layout("west_plaza_topiary_2022", BuildingSymmetrical, 8, 10, 4, 8, 6)
    make_object_layout("west_plaza_topiary_2023", BuildingSymmetrical, 6, 16, 2, 10, 10)
    make_object_layout("west_plaza_topiary_2024a", BuildingSymmetrical, 8, 12, 2, 2, 6, BuildingCylindrical)
    make_object_layout("west_plaza_topiary_2024b", BuildingSymmetrical, 8, 12, 2, 2, 6, BuildingCylindrical)