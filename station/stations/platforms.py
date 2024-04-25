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
        prefix="station/voxels/render/csps",
        voxel_getter=lambda path=f"station/voxels/csps/{name}.vox": path,
        load_from="station/files/csps-gorender.json",
    )

    platform_components = {"side_platform", "platform"}
    shed_components = {"shed", "shed_building", "pillar"}

    for platform_flavor, traversable, pkeeps, pheight in [
        ("np", True, set(), 0),
        ("", True, {"platform"}, platform_height),
        ("_side", False, {"side_platform"}, platform_height),
    ]:
        for shed_flavor, symmetry, skeeps, sheight in [
            ("", BuildingSpriteSheetSymmetricalX, set(), 0),
            ("_shed", BuildingSpriteSheetSymmetricalX, {"shed"}, shed_height),
            ("_shed_building", BuildingSpriteSheetFull, {"shed_building"}, shed_height),
            ("_pillar", BuildingSpriteSheetSymmetricalX, {"pillar"}, pillar_height),
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
named_tiles = AttrDict()

for name in ["pl1_low_white"]:
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
        Demo("Platform", [[pl1_low_white], [pl1_low_white_d], [pl1_low_white.T]]),
        Demo("Platform with concrete grounds", [[pl1_low_white_side], [pl1_low_white_d], [pl1_low_white_side.T]]),
        Demo("Platform with shed", [[pl1_low_white_shed], [pl1_low_white_shed_d], [pl1_low_white_shed.T]]),
    ],
)
