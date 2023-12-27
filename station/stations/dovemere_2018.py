import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "dovemere_2018",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018.vox",
    load_from="station/files/gorender.json",
)
vox.render()
voxels = [LazySpriteSheet([vox], [(0, 0)])]

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=[s for v in voxels for s in v.spritesheet(0, 0)] * 18,
    class_label=b"2018",
    cargo_threshold=40,
    callbacks={
        "availability": grf.DefaultCallback(
            default=1,
        ),
    },
)
