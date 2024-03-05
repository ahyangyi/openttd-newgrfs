from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "front_normal",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018/front_normal.vox",
    load_from="station/files/gorender.json",
)
vox.render()
voxels = [LazySpriteSheet([vox], [(0, 0)])]

the_station = AStation(
    id=0x01,
    translation_name="DOVEMERE_1992",
    sprites=[s for v in voxels for s in v.spritesheet(0, 0)] * 18,
    cargo_threshold=40,
    class_label=b"CONC",
)
