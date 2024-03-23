import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    Demo,
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
    ret = type.from_complete_list(v.spritesheet(xdiff=10))
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


def simple_layout(ground_sprite, sprite_id, flag):
    layouts = [
        grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=ground_sprite,
                pal=0,
                is_global=True,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        ),
    ]
    if flag & 1:
        layouts.append(
            grf.ParentSprite(
                sprite=grf.SpriteRef(
                    id=0x42D + sprite_id,
                    pal=0,
                    is_global=False,
                    use_recolour=True,
                    always_transparent=False,
                    no_transparent=False,
                ),
                extent=(16, 6, 6) if sprite_id % 2 == 0 else (6, 16, 6),
                offset=(0, 10, 0) if sprite_id % 2 == 0 else (10, 0, 0),
                flags=0,
            )
        )
    if flag & 2:
        layouts.append(
            grf.ParentSprite(
                sprite=grf.SpriteRef(
                    id=0x42D + sprite_id + 2,
                    pal=0,
                    is_global=False,
                    use_recolour=True,
                    always_transparent=False,
                    no_transparent=False,
                ),
                extent=(16, 6, 6) if sprite_id % 2 == 0 else (6, 16, 6),
                offset=(0, 0, 0),
                flags=0,
            ),
        )
    return grf.SpriteLayout(layouts)


the_stations = AMetaStation(
    [
        AStation(
            id=0xF0 + var,
            translation_name="DOVEMERE_2018",  # FIXME
            sprites=[s for s, _ in layouts],
            layouts=[
                simple_layout(1012 - i % 2 if traversable else 1420, i, 1 + var)
                for i, (s, traversable) in enumerate(layouts[:2])
            ],
            class_label=b"PLAT",
            cargo_threshold=40,
            callbacks={
                "select_tile_layout": 0,
            },
        )
        for var in range(3)
    ],
    b"PLAT",
    [layouts[0][0] for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))],
    [
        Demo("Test", [[pl1_low_white]]),
    ],
)
