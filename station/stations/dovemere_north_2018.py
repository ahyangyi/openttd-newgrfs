import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingFull,
    BuildingSymmetrical,
    BuildingSymmetricalX,
    BuildingSymmetricalY,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from .platforms import platform_ps, platform_width


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_north_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_north_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
        config={"z_scale": 1.0},
    )
    sprite = type.create_variants(v.spritesheet(zdiff=16, xdiff=platform_width, xspan=16 - platform_width))

    ground = ADefaultGroundSprite(1420)
    parent = AParentSprite(sprite, (16, 16 - platform_width, 48), (0, platform_width, 0))
    plat = platform_ps.cns_concrete_side_shelter_2.up(8)

    candidates = [ALayout(ground, [plat.T, parent], False)]

    ret = []
    for l in candidates:
        l = type.get_all_variants(l)
        layouts.extend(l)
        ret.append(type.create_variants(l))

    if len(ret) == 1:
        return ret[0]
    return ret


layouts = []
(front_normal,) = [
    quickload(name, type, traversable) for name, type, traversable in [("front_normal", BuildingSymmetricalX, False)]
]


the_stations = AMetaStation(
    [
        AStation(
            id=0x3000 + i,
            translation_name="BUILDING",
            layouts=layouts,
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
    [Demo("Test", [[front_normal, front_normal]])],
)
