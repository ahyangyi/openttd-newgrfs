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
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from station.lib.parameters import station_cb
from .misc import building_ground


def quickload(name, symmetry):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1934",
        voxel_getter=lambda path=f"station/voxels/dovemere_1934/{name}.vox": path,
        load_from="station/files/gorender.json",
        config={"agrf_palette": "station/files/dovemere_1934_palette.json", "z_scale": 1.0},
        subset=symmetry.render_indices(),
    )
    sprite = symmetry.create_variants(v.spritesheet(xdiff=1))
    ps = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    l = ALayout([building_ground], [ps], False)
    var = symmetry.get_all_variants(l)
    ret = symmetry.create_variants(var)
    entries.extend(symmetry.get_all_entries(ret))
    named_tiles[name] = ret


entries = []
named_tiles = AttrDict()
for name, symmetry in [("regular", BuildingSpriteSheetSymmetricalX)]:
    quickload(name, symmetry)

the_stations = AMetaStation(
    [
        AStation(
            id=0x2000 + i,
            translation_name="PLATFORM" if entry.traversable else "PLATFORM_UNTRAVERSABLE",
            layouts=[entry, entry.M],
            class_label=b"\xe8\x8a\x9c0",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0, **station_cb["E88A9C0"]},
        )
        for i, entry in enumerate(entries)
    ],
    b"\xe8\x8a\x9c0",
    None,
    entries,
    [Demo("The building", [[named_tiles.regular]])],
)