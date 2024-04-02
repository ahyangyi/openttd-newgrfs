import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from .platforms import sprites as platform_sprites


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.create_variants(v.spritesheet(zdiff=16))
    sprites.extend(sprite.all_variants)

    ground = ADefaultGroundSprite(1012 if traversable else 1420)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    plat = AParentSprite(platform_sprites[0].T, (16, 6, 6), (0, 0, 8))
    candidates = [ALayout(ground, [plat, parent], False)]

    ret = []
    for l in candidates:
        l = type.get_all_variants(l)
        layouts.extend(l)
        ret.append(type.create_variants(l))

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = platform_sprites.copy()
layouts = []
(front_normal,) = [
    quickload(name, type, traversable)
    for name, type, traversable in [("front_normal", BuildingSpriteSheetSymmetricalX, False)]
]


the_stations = AMetaStation(
    [
        AStation(
            id=0x80 + i,
            translation_name="UNTRAVERSABLE",
            sprites=sprites,  # FIXME
            layouts=[layouts[0].to_grf(sprites), layouts[1].to_grf(sprites)],
            class_label=b"\xe9\xb8\xa0A",
            cargo_threshold=40,
            non_traversable_tiles=0b11,
            # general_flags=0x08, # FIXME: handle custom foundation later
            callbacks={"select_tile_layout": 0},
        )
        for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"\xe9\xb8\xa0A",
    [None],
    layouts,
    [Demo("Test", [[front_normal, front_normal]])],
)
