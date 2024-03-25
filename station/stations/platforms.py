import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/csps",
        voxel_getter=lambda path=f"station/voxels/csps/{name}.vox": path,
        load_from="station/files/csps-gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.create_variants(v.spritesheet(xdiff=10))
    sprites.extend(sprite.all_variants)

    ps = AParentSprite(sprite, (16, 6, 6), (0, 10, 0))
    ret = [
        ALayout(ADefaultGroundSprite(1012), [ps]),
        ALayout(ADefaultGroundSprite(1011), [ps.M]),
        ALayout(ADefaultGroundSprite(1012), [ps.T]),
        ALayout(ADefaultGroundSprite(1011), [ps.T.M]),
        ALayout(ADefaultGroundSprite(1012), [ps, ps.T]),
        ALayout(ADefaultGroundSprite(1011), [ps.M, ps.T.M]),
    ]

    layouts.extend(ret)
    return ret


sprites = []
layouts = []
[(pl1_low_white, pl1_low_white_m, pl1_low_white_t, pl1_low_white_t_m, pl1_low_white_d, pl1_low_white_d_m)] = [
    quickload(name, type, traversable)
    for name, type, traversable in [("pl1_low_white", BuildingSpriteSheetSymmetricalX, True)]
]


the_stations = AMetaStation(
    [
        AStation(
            id=0xF0 + i,
            translation_name="DOVEMERE_2018",  # FIXME
            sprites=sprites,  # FIXME
            layouts=[layout[0].to_grf(sprites), layout[1].to_grf(sprites)],
            class_label=b"PLAT",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0},
        )
        for i, layout in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"PLAT",
    layouts,
    [Demo("Test", [[pl1_low_white], [pl1_low_white_d], [pl1_low_white_t]])],
)
