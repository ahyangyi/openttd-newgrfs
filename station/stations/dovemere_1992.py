import grf
from station.lib import AStation, AMetaStation, BuildingSpriteSheetSymmetricalX, Demo, simple_layout
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1992",
        voxel_getter=lambda path=f"station/voxels/dovemere_1992/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    ret = type.from_complete_list(v.spritesheet())
    sprites.extend(ret.all_variants)
    for sprite in ret.all_variants:
        layouts.append((sprite, traversable))
    return ret


sprites = []
layouts = []
(main,) = [
    quickload(name, type, traversable) for name, type, traversable in [("main", BuildingSpriteSheetSymmetricalX, False)]
]

the_station = AStation(
    id=0x100,
    translation_name="DOVEMERE_1992",
    sprites=sprites,
    layouts=[
        simple_layout(1012 - i % 2 if traversable else 1420, sprites.index(s))
        for i, (s, traversable) in enumerate(layouts)
    ],
    cargo_threshold=40,
    class_label=b"DM92",
)
the_stations = AMetaStation(
    [the_station],
    b"DM92",
    [layouts[0][0] for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))],
    [Demo("Station", [[main]])],
)
