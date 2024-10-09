from industry.lib.industry_tile import AIndustryTile
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "one_tile_flat",
    prefix=".cache/render/industry/one_tile_flat",
    voxel_getter=lambda: "industry/voxels/one_tile_flat.vox",
    load_from="industry/files/gorender.json",
)
rotated_voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(4)]


the_industry_tile = AIndustryTile(
    id=0x23, sprites=[s for v in rotated_voxels for s in v.spritesheet()], substitute_type=0
)
