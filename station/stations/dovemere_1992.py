import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSymmetricalX,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
    LayoutSprite,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch


def quickload(name, sym, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1992",
        voxel_getter=lambda path=f"station/voxels/dovemere_1992/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(v.spritesheet())
    ground = ADefaultGroundSprite(1012 if traversable else 1420)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    candidates = [ALayout(ground, [parent], False)]
    ret = []
    for l in candidates:
        l = sym.get_all_variants(l)
        layouts.extend(l)
        l = sym.create_variants(l)
        ret.append(l)
        entries.extend(sym.get_all_entries(l))

    if len(ret) == 1:
        return ret[0]
    return ret


layouts = []
entries = []
(main,) = [quickload(name, sym, traversable) for name, sym, traversable in [("main", BuildingSymmetricalX, False)]]

the_station = AStation(
    id=0x1000,
    translation_name="PLATFORM_UNTRAVERSABLE",
    layouts=layouts,
    class_label=b"\xe8\x8a\x9ca",
    cargo_threshold=40,
)
the_stations = AMetaStation([the_station], b"\xe8\x8a\x9ca", None, [Demo("Station", [[main]])])
