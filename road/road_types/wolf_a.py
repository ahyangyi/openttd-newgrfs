from road.lib import ARoadType
from datetime import date
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
    id=0x01,
    name="Wolf A",
    label=b"WOLF",
    introduction_date=date(1920, 1, 1),
    sprites=spritesheet.spritesheet(0, 0),
)
