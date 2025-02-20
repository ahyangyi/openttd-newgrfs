from agrf.graphics.voxel import LazyVoxel
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingCylindrical,
    BuildingDiagonalAlt,
    AParentSprite,
    AChildSprite,
    AttrDict,
    Registers,
)
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR


components = AttrDict(schema=("type", "name"))


def make_component(dirname, name, sym, span, offset, has_nosnow=False):
    v = LazyVoxel(
        name,
        prefix=f".cache/render/station/dovemere_2018/west_plaza/{dirname}",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/west_plaza/{dirname}/{name}.vox": path,
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

    components[(dirname, name)] = gs


def make_components():
    pass
