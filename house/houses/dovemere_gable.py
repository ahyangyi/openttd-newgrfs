from house.lib import AHouse
from pygorender import Config, render
import grf
from agrf.graphics.voxel import LazyVoxel

vox = LazyVoxel(
    "dovemere_gable",
    prefix=f"house/voxels/render/dovemere_gable",
    voxel_getter=lambda: f"house/voxels/dovemere_gable.vox",
    load_from="house/files/gorender.json",
)
vox.render()


the_house = AHouse(
    id=0x80,
    name="House",
    sprites=vox.spritesheet(0, 0),
    flags=0x1,
    availability_mask=0xF81F,
)
