from road.lib import ARoadType
from pygorender import Config, render
import grf
from agrf.graphics.voxel import LazyVoxel

vox = LazyVoxel(
    "wolf_a",
    prefix=f"road/voxels/render/wolf_a",
    voxel_getter=lambda: f"road/voxels/wolf_a/straight.vox",
    load_from="road/files/gorender.json",
)
vox.render()


the_road = ARoadType(
    id=0x80,
    name="RoadType",
    sprites=vox.spritesheet(0, 0),
    flags=0x1,
    availability_mask=0xF81F,
)
