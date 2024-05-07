from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetFull,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from .ground import named_ps as ground_ps


gray_ps = ground_ps.gray


platform_height = 4
platform_width = 5
shed_height = 13
pillar_height = 14


shed_meta = [
    ("", BuildingSpriteSheetSymmetricalX, set(), 0, True),
    ("_shed", BuildingSpriteSheetSymmetricalX, {"shed"}, shed_height, True),
    ("_shed_building", BuildingSpriteSheetFull, {"shed_building"}, shed_height, False),
    ("_shed_building_v", BuildingSpriteSheetSymmetricalX, {"shed_building_v"}, shed_height, False),
    ("_pillar", BuildingSpriteSheetSymmetricalX, {"pillar"}, pillar_height, False),
    ("_pillar_building", BuildingSpriteSheetFull, {"pillar_building"}, pillar_height, False),
    ("_pillar_central", BuildingSpriteSheetSymmetricalX, {"pillar_central"}, pillar_height, False),
]


def quickload(name):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/cnsps",
        voxel_getter=lambda path=f"station/voxels/cnsps/{name}.vox": path,
        load_from="station/files/cnsps-gorender.json",
    )

    platform_components = {
        "white",
        "white_side",
        "modernnarrow",
        "modernnarrow_side",
        "modernnarrow_cut",
        "modernnarrow_high",
        "modernnarrow_high_side",
    }
    shed_components = {"shed", "shed_building", "shed_building_v", "pillar", "pillar_building", "pillar_central"}

    for platform_flavor, traversable, pkeeps, pheight in [
        ("_np", True, set(), 0),
        ("", True, {"modernnarrow"}, platform_height),
        ("_side", False, {"modernnarrow_side"}, platform_height),
        ("_cut", False, {"modernnarrow_cut"}, platform_height),
    ]:
        for shed_flavor, symmetry, skeeps, sheight, buildable in shed_meta:
            if (platform_flavor, shed_flavor) == ("_np", ""):
                # Don't create the "nothing" tile
                continue

            suffix = platform_flavor + shed_flavor
            v2 = v.discard_layers(
                tuple(sorted(tuple(platform_components - pkeeps) + tuple(shed_components - skeeps))), "subset" + suffix
            )
            v2.in_place_subset(symmetry.render_indices())
            foundation_height = platform_height if shed_flavor == "_cut" else 0
            sprite = symmetry.create_variants(v2.spritesheet(xdiff=16 - platform_width, zdiff=foundation_height * 2))

            height = max(pheight, sheight)
            ps = AParentSprite(
                sprite, (16, platform_width, height - foundation_height), (0, 16 - platform_width, foundation_height)
            )
            named_ps[name + suffix] = ps

            for l, make_symmetrical, extra_suffix in [([ps], False, ""), ([ps, ps.T], True, "_d")]:
                groundsprite = ADefaultGroundSprite(1012) if traversable else gray_ps
                if make_symmetrical:
                    cur_symmetry = symmetry.add_y_symmetry()
                else:
                    cur_symmetry = symmetry
                var = cur_symmetry.get_all_variants(ALayout([groundsprite], l, traversable))
                l = cur_symmetry.create_variants(var)
                if buildable and platform_flavor != "_np":
                    entries.extend(cur_symmetry.get_all_entries(l))
                named_tiles[name + suffix + extra_suffix] = l


def simple_load(name, symmetry):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/cnsps",
        voxel_getter=lambda path=f"station/voxels/cnsps/{name}.vox": path,
        load_from="station/files/cnsps-gorender.json",
        subset=symmetry.render_indices(),
    )
    sprite = symmetry.create_variants(v.spritesheet())
    ps = AParentSprite(sprite, (16, 16, platform_height), (0, 0, 0))
    named_ps[name] = ps

    groundsprite = gray_ps
    var = symmetry.get_all_variants(ALayout([groundsprite], [ps], False, notes={"concourse"}))
    l = symmetry.create_variants(var)
    entries.extend(symmetry.get_all_entries(l))
    named_tiles[name] = l

    for shed_flavor, symmetry, skeeps, sheight, buildable in shed_meta:
        if shed_flavor == "":
            continue
        var = symmetry.get_all_variants(
            ALayout([groundsprite], [ps, named_ps["cnsps_cut" + shed_flavor]], False, notes={"concourse"})
        )
        l = symmetry.create_variants(var)
        entries.extend(symmetry.get_all_entries(l))
        named_tiles[name + shed_flavor] = l


entries = []
named_ps = AttrDict()
named_tiles = AttrDict()

quickload("cnsps")
simple_load("concourse", BuildingSpriteSheetSymmetrical)
simple_load("side_concourse", BuildingSpriteSheetSymmetricalX)

named_tiles.globalize()

the_stations = AMetaStation(
    [
        AStation(
            id=0xF000 + i,
            translation_name=(
                "CONCOURSE"
                if "concourse" in entry.notes
                else "PLATFORM" if entry.traversable else "PLATFORM_UNTRAVERSABLE"
            ),
            layouts=[entry, entry.M],
            class_label=b"PLAT",
            cargo_threshold=40,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={"select_tile_layout": 0},
        )
        for i, entry in enumerate(entries)
    ],
    b"PLAT",
    None,
    entries,
    [
        Demo("Platform", [[cnsps], [cnsps_d], [cnsps.T]]),
        Demo("Platform with concrete grounds", [[cnsps_side], [cnsps_d], [cnsps_side.T]]),
        Demo("Platform with shed", [[cnsps_shed], [cnsps_shed_d], [cnsps_shed.T]]),
    ],
)
