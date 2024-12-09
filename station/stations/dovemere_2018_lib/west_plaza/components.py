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
from ..objects_utils import objects, register_slopes, DEFAULT_FLAGS, named_layouts, register


components = AttrDict(schema=("name",))


def make_component(name, sym, span, offset, has_nosnow=False):
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

    components[(name.replace("west_plaza_", ""),)] = gs


def make_components():
    make_component("west_plaza_planter_1", BuildingFull, (4, 3, 1), (2, 11, 0))
    make_component("west_plaza_planter_2", BuildingFull, (7, 3, 1), (2, 11, 0))
    make_component("west_plaza_pole", BuildingCylindrical, (2, 2, 8), (7, 7, 0))
    make_component("west_plaza_underground_entrance", BuildingFull, (4, 4, 8), (6, 6, 0))
    make_component("corner_lawn", BuildingFull, (6, 6, 1), (10, 0, 0))
    make_component("edge_lawn", BuildingSymmetricalX, (16, 6, 1), (0, 0, 0))
    make_component("split_lawn", BuildingFull, (16, 6, 1), (0, 10, 0))
    make_component("west_plaza_tree_bench", BuildingFull, (2, 2, 8), (7, 7, 0), has_nosnow=True)
    make_component("west_plaza_tree_bush", BuildingFull, (2, 2, 8), (7, 7, 0), has_nosnow=True)
    make_component("west_plaza_glass_pyramid", BuildingSymmetrical, (2, 2, 8), (7, 7, 0))
