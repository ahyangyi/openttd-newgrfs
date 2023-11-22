from industry.lib.industry_tile import AIndustryTile
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "one_tile_flat",
    prefix=f"industry/voxels/render/one_tile_flat",
    voxel_getter=lambda: f"industry/voxels/one_tile_flat.vox",
    load_from="industry/files/gorender.json",
)
vox.render()
rotated_voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(4)]


the_industry_tile = AIndustryTile(
    id=0x23, sprites=[s for v in rotated_voxels for s in v.spritesheet(0, 0)], building_type=0
)
