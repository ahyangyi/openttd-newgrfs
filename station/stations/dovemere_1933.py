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
from .ground import gray


def quickload(name, type):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1933",
        voxel_getter=lambda path=f"station/voxels/dovemere_1933/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.create_variants(v.spritesheet())
    groundsprite = AGroundSprite(gray)
    ps = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    l = ALayout([groundsprite], [ps], False)
    var = type.get_all_variants(l)
    layouts.extend(var)
    return type.create_variants(var)


layouts = []
[front_normal] = [quickload(name, type) for name, type in [("front_normal", BuildingSpriteSheetSymmetricalX)]]

the_stations = AMetaStation(
    [
        AStation(
            id=0x2000 + i,
            translation_name="PLATFORM" if layout[0].traversable else "PLATFORM_UNTRAVERSABLE",
            layouts=layout,
            class_label=b"\xe8\x8a\x9c0",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0},
        )
        for i, layout in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"\xe8\x8a\x9c0",
    None,
    layouts,
    [],
)
