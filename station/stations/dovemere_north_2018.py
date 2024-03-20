import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    Demo,
    simple_layout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    ret = type.from_complete_list(v.spritesheet())
    sprites.extend(ret.all_variants)
    for sprite in ret.all_variants:
        layouts.append((sprite, traversable))
    return ret


sprites = []
layouts = []
(front_normal,) = [
    quickload(name, type, traversable)
    for name, type, traversable in [
        ("front_normal", BuildingSpriteSheetSymmetricalX, False),
    ]
]


the_stations = AMetaStation(
    [
        AStation(
            id=0x80 + i,
            translation_name="DOVEMERE_NORTH_2018",  # FIXME
            sprites=[s for s, _ in layouts] * 4,  # FIXME create actual foundation graphics
            layouts=[
                simple_layout(1012 - i % 2 if traversable else 1420, i) for i, (s, traversable) in enumerate(layouts)
            ],
            class_label=b"DN18",
            cargo_threshold=40,
            non_traversable_tiles=0b00 if layouts[0][1] else 0b11,
            general_flags=0x08,
            callbacks={
                "select_tile_layout": 0,
            },
        )
        for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"DN18",
    [layouts[0][0] for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))],
    [
        Demo(
            "Test",
            [[front_normal, front_normal]],
        ),
    ],
)
