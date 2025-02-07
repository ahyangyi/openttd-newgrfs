from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from station.lib import AttrDict, AParentSprite, AChildSprite, BuildingFull, Registers
from agrf.graphics.voxel import LazyVoxel

aux_ps = AttrDict(schema=("name",))

v = LazyVoxel(
    "bufferstop",
    prefix=".cache/render/station/cns",
    voxel_getter=lambda path="station/voxels/cns/bufferstop.vox": path,
    load_from="station/files/cns-gorender.json",
)
symmetry = BuildingFull
nosnow = v.discard_layers(("snow",), "nosnow")
snow = v.keep_layers(("snow",), "snow")
snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
snow.config["overlap"] = 1.3

nosnow.in_place_subset(symmetry.render_indices())
nosnow.config["agrf_manual_crop"] = (0, 20)
nosnow_sprite = symmetry.create_variants(nosnow.spritesheet(xspan=6, xdiff=10, yspan=6, ydiff=5))

snow.in_place_subset(symmetry.render_indices())
snow.config["agrf_childsprite"] = (0, -20)
snow_sprite = symmetry.create_variants(snow.spritesheet(xspan=6, xdiff=10, yspan=6, ydiff=5))

ps = AParentSprite(nosnow_sprite, (6, 6, 4), (5, 10, 0)).M.R
cs = AChildSprite(snow_sprite, (0, 0), flags={"dodraw": Registers.SNOW}).M.R

aux_ps[("bufferstop",)] = bufferstop = ps + cs
