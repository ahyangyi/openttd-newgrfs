from road.lib import ARoadType
from pygorender import Config, render
import grf
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

voxels = [
    LazyVoxel(
        k,
        prefix=f"road/voxels/render/wolf_a",
        voxel_getter=lambda k=k: f"road/voxels/wolf_a/{k}.vox",
        load_from="road/files/gorender.json",
    )
    for k in ["straight", "crossroad", "junction", "curve", "end"]
]
spritesheet = LazySpriteSheet(
    voxels,
    [
        (0, 0),
        (0, 1),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (2, 3),
        (3, 0),
        (3, 1),
        (3, 2),
        (3, 3),
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
        (4, 0),
        (4, 1),
        (4, 2),
        (4, 3),
    ],
)
spritesheet.render()


the_road = ARoadType(
    id=0x80,
    name="RoadType",
    sprites=spritesheet.spritesheet(0, 0),
    flags=0x1,
    availability_mask=0xF81F,
)
