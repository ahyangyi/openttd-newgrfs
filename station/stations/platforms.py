from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetrical,
    Demo,
    ADefaultGroundSprite,
    AGroundSprite,
    AParentSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from .ground import sprites as ground_sprites, gray


def quickload(name, type):
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
    ret = []
    for l, make_symmetrical in [([ps], False), ([ps, ps.T], True)]:
        for traversable in [True, False]:
            groundsprite = ADefaultGroundSprite(1012) if traversable else AGroundSprite(gray)
            cur_type = BuildingSpriteSheetSymmetrical if make_symmetrical else type
            var = cur_type.get_all_variants(ALayout(groundsprite, l, True))
            layouts.extend(var)
            ret.append(cur_type.create_variants(var))

    return ret


sprites = []
layouts = []
[(pl1_low_white, pl1_low_white_nt, pl1_low_white_d, pl1_low_white_d_nt)] = [
    quickload(name, type) for name, type in [("pl1_low_white", BuildingSpriteSheetSymmetricalX)]
]
sprites = sprites + ground_sprites
for i, s in enumerate(sprites):
    print(i, s)
for i, l in enumerate(layouts):
    print(i, l)

the_stations = AMetaStation(
    [
        AStation(
            id=0xF0 + i,
            translation_name="PLATFORM",
            sprites=sprites,  # FIXME
            layouts=[layout[0].to_grf(sprites), layout[1].to_grf(sprites)],
            class_label=b"PLAT",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0},
        )
        for i, layout in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"PLAT",
    None,
    layouts,
    [
        Demo("Test", [[pl1_low_white], [pl1_low_white_d], [pl1_low_white.T]]),
        Demo("Test", [[pl1_low_white_nt], [pl1_low_white_d], [pl1_low_white_nt.T]]),
    ],
)
