from station.lib import AttrDict, AParentSprite, BuildingFull
from agrf.graphics.voxel import LazyVoxel

aux_ps = AttrDict(schema=("name",))

v = LazyVoxel(
    "bufferstop",
    prefix=".cache/render/station/cns",
    voxel_getter=lambda path="station/voxels/cns/bufferstop.vox": path,
    load_from="station/files/cns-gorender.json",
)
symmetry = BuildingFull
v.in_place_subset(symmetry.render_indices())
s = symmetry.create_variants(v.spritesheet(xspan=6, xdiff=10, yspan=6, ydiff=5))
ps = AParentSprite(s, (6, 6, 4), (10, 5, 0))

aux_ps[("bufferstop",)] = bufferstop = ps
