import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet
from agrf.sprites import number_alternatives

vox = LazyVoxel(
    "dovemere_2018",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018.vox",
    load_from="station/files/gorender.json",
)
vox.render()
voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(4)]

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=[number_alternatives(voxels[i % 2 + 2].spritesheet(0, 0)[0], i) for i in range(100)],
    class_label=b"2018",
    cargo_threshold=40,
    callbacks={
        "availability": grf.DefaultCallback(
            default=1,
        ),
    },
)
