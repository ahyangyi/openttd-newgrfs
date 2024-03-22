import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    Demo,
    simple_layout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/csps",
        voxel_getter=lambda path=f"station/voxels/csps/{name}.vox": path,
        load_from="station/files/csps-gorender.json",
    )
    ret = type.from_complete_list(v.spritesheet())
    sprites.extend(ret.all_variants)
    for sprite in ret.all_variants:
        layouts.append((sprite, traversable))
    return ret


sprites = []
layouts = []
(pl1_low_white,) = [
    quickload(name, type, traversable)
    for name, type, traversable in [
        ("pl1_low_white", BuildingSpriteSheetSymmetricalX, True),
    ]
]


the_stations = AMetaStation(
    [
        AStation(
            id=0xF0 + i,
            translation_name="DOVEMERE_2018",  # FIXME
            sprites=[s for s, _ in layouts],
            layouts=[
                simple_layout(1012 - i % 2 if traversable else 1420, i) for i, (s, traversable) in enumerate(layouts)
            ],
            class_label=b"PLAT",
            cargo_threshold=40,
            non_traversable_tiles=0b00 if layouts[0][1] else 0b11,
            callbacks={
                "select_tile_layout": 0,
            },
        )
        for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"PLAT",
    [layouts[0][0] for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))],
    [
        Demo("Test", [[pl1_low_white]]),
    ],
)
