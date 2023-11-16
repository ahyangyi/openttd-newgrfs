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
    sprites=[s for v in voxels for s in v.spritesheet(0, 0)],
    **{"class": b"2018"},
)
