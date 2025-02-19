from house.lib import AHouse
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "dovemere_gable",
    prefix=".cache/render/house/dovemere_gable",
    voxel_getter=lambda: "house/voxels/dovemere_gable.vox",
    load_from="house/files/gorender.json",
)
vox.render()
rotated_voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(4)]


the_house = AHouse(
    substitute=0x06,
    id=0x80,
    name="House",
    sprites=[s for v in rotated_voxels for s in v.spritesheet()],
    flags=0x1,
    availability_mask=0xF81F,
)
