from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetFull,
    Demo,
    ADefaultGroundSprite,
    AGroundSprite,
    AParentSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from .ground import gray


platform_height = 6
shed_height = 13
pillar_height = 14


def quickload(name):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/cnsps",
        voxel_getter=lambda path=f"station/voxels/cnsps/{name}.vox": path,
        load_from="station/files/cnsps-gorender.json",
    )

    platform_components = {"white", "white_side", "modernnarrow", "modernnarrow_side"}
    shed_components = {"shed", "shed_building", "shed_building_v", "pillar", "pillar_building", "pillar_central"}

    for platform_flavor, traversable, pkeeps, pheight in [
        ("_np", True, set(), 0),
        ("", True, {"modernnarrow"}, platform_height),
        ("_side", False, {"modernnarrow_side"}, platform_height),
    ]:
        for shed_flavor, symmetry, skeeps, sheight in [
            ("", BuildingSpriteSheetSymmetricalX, set(), 0),
            ("_shed", BuildingSpriteSheetSymmetricalX, {"shed"}, shed_height),
            ("_shed_building", BuildingSpriteSheetFull, {"shed_building"}, shed_height),
            ("_shed_building_v", BuildingSpriteSheetSymmetricalX, {"shed_building_v"}, shed_height),
            ("_pillar", BuildingSpriteSheetSymmetricalX, {"pillar"}, pillar_height),
            ("_pillar_building", BuildingSpriteSheetFull, {"pillar_building"}, pillar_height),
            ("_pillar_central", BuildingSpriteSheetSymmetricalX, {"pillar_central"}, pillar_height),
        ]:
            suffix = platform_flavor + shed_flavor
            v2 = v.discard_layers(
                tuple(sorted(tuple(platform_components - pkeeps) + tuple(shed_components - skeeps))), "subset" + suffix
            )
            v2.in_place_subset(symmetry.render_indices())
            sprite = symmetry.create_variants(v2.spritesheet(xdiff=10))
            named_sprites[name + suffix] = sprite

            height = max(pheight, sheight)
            ps = AParentSprite(sprite, (16, 6, height), (0, 10, 0))
            named_ps[name + suffix] = ps

            for l, make_symmetrical, extra_suffix in [([ps], False, ""), ([ps, ps.T], True, "_d")]:
                groundsprite = ADefaultGroundSprite(1012) if traversable else AGroundSprite(gray)
                if make_symmetrical:
                    cur_symmetry = symmetry.add_y_symmetry()
                else:
                    cur_symmetry = symmetry
                var = cur_symmetry.get_all_variants(ALayout([groundsprite], l, True))
                layouts.extend(var)
                l = cur_symmetry.create_variants(var)
                named_tiles[name + suffix + extra_suffix] = l


layouts = []
named_sprites = AttrDict()
named_ps = AttrDict()
named_tiles = AttrDict()

for name in ["cnsps"]:
    quickload(name)

named_tiles.globalize()

the_stations = AMetaStation(
    [
        AStation(
            id=0xF000 + i,
            translation_name="PLATFORM" if layout[0].traversable else "PLATFORM_UNTRAVERSABLE",
            layouts=layout,
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
        Demo("Platform", [[cnsps], [cnsps_d], [cnsps.T]]),
        Demo("Platform with concrete grounds", [[cnsps_side], [cnsps_d], [cnsps_side.T]]),
        Demo("Platform with shed", [[cnsps_shed], [cnsps_shed_d], [cnsps_shed.T]]),
    ],
)
