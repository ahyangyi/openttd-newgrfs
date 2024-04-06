import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
    LayoutSprite,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1992",
        voxel_getter=lambda path=f"station/voxels/dovemere_1992/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    sprite = type.create_variants(v.spritesheet())
    sprites.extend(sprite.all_variants)
    ground = ADefaultGroundSprite(1012 if traversable else 1420)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    candidates = [ALayout(ground, [parent])]
    ret = []
    for l in candidates:
        l = type.get_all_variants(l)
        layouts.extend(l)
        ret.append(type.create_variants(l))

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = []
layouts = []
(main,) = [
    quickload(name, type, traversable) for name, type, traversable in [("main", BuildingSpriteSheetSymmetricalX, False)]
]

the_station = AStation(
    id=0x1000,
    translation_name="UNTRAVERSABLE",
    sprites=sprites,
    layouts=[layout.to_grf(sprites) for layout in layouts],
    class_label=b"\xe8\x8a\x9ca",
    cargo_threshold=40,
)
the_stations = AMetaStation([the_station], b"\xe8\x8a\x9ca", None, layouts, [Demo("Station", [[main]])])
