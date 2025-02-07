from station.lib import AttrDict, AParentSprite, BuildingFull

aux_ps = AttrDict(schema=("name",))

v = LazyVoxel(
    "bufferstop",
    prefix=".cache/render/station/cns",
    voxel_getter=lambda path="station/voxels/cns/bufferstop.vox": path,
    load_from="station/files/cns-gorender.json",
)
symmetry = BuildingFull
v.in_place_subset(symmetry.render_indices())
s = symmetry.create_variants(v.spritesheet())
ps = AParentSprite(s, (5, 5, 0), (6, 6, 4))

aux_ps[("bufferstop",)] = ps
