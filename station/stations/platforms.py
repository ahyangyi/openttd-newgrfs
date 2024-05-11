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
shed_height = 17
pillar_height = 18


plat_meta = [
    ("_np", False, set(), 0),
    ("", True, {"modernnarrow"}, platform_height),
    ("_side", True, {"modernnarrow_side"}, platform_height),
    ("_cut", False, {"modernnarrow_cut"}, platform_height),
]


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
        prefix="station/voxels/render/cns",
        voxel_getter=lambda path=f"station/voxels/cns/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )

    platform_components = {"modernnarrow", "modernnarrow_side"}
    shed_components = {"shed", "shed_building", "shed_building_v", "pillar", "pillar_building", "pillar_central"}

    for platform_flavor, pbuildable, pkeeps, pheight in plat_meta:
        for shed_flavor, symmetry, skeeps, sheight, sbuildable in shed_meta:
            if (platform_flavor, shed_flavor) == ("_np", ""):
                # Don't create the "nothing" tile
                continue

            suffix = platform_flavor + shed_flavor
            v2 = v.discard_layers(
                tuple(sorted(tuple(platform_components - pkeeps) + tuple(shed_components - skeeps))), "subset" + suffix
            )
            v2.in_place_subset(symmetry.render_indices())
            foundation_height = platform_height if platform_flavor == "_cut" else 0
            sprite = symmetry.create_variants(
                v2.spritesheet(xdiff=16 - platform_width, xspan=platform_width, zdiff=foundation_height * 2)
            )

            height = max(pheight, sheight)
            ps = AParentSprite(
                sprite, (16, platform_width, height - foundation_height), (0, 16 - platform_width, foundation_height)
            )
            named_ps[name + suffix] = ps

            for l, make_symmetrical, extra_suffix in [([ps], False, ""), ([ps, ps.T], True, "_d")]:
                groundsprite = ADefaultGroundSprite(1012)
                if make_symmetrical:
                    cur_symmetry = symmetry.add_y_symmetry()
                else:
                    cur_symmetry = symmetry
                var = cur_symmetry.get_all_variants(ALayout([groundsprite], l, True))
                l = cur_symmetry.create_variants(var)
                if sbuildable and pbuildable:
                    entries.extend(cur_symmetry.get_all_entries(l))
                named_tiles[name + suffix + extra_suffix] = l

    for platform_flavor, pbuildable, pkeeps, pheight in plat_meta:
        if pbuildable:
            for shed_flavor, symmetry, skeeps, sheight, sbuildable in shed_meta:
                if sbuildable:
                    for platform_flavor_2, pbuildable_2, _, _ in plat_meta:
                        if pbuildable_2:
                            for shed_flavor_2, _, _, sheight_2, sbuildable_2 in shed_meta:
                                if sbuildable_2 and (
                                    (platform_flavor, shed_flavor) < (platform_flavor_2, shed_flavor_2)
                                ):
                                    groundsprite = ADefaultGroundSprite(1012)
                                    cur_symmetry = BuildingSpriteSheetSymmetricalX
                                    var = cur_symmetry.get_all_variants(
                                        ALayout(
                                            [groundsprite],
                                            [
                                                named_ps[name + platform_flavor + shed_flavor],
                                                named_ps[name + platform_flavor_2 + shed_flavor_2].T,
                                            ],
                                            True,
                                        )
                                    )
                                    l = cur_symmetry.create_variants(var)
                                    entries.extend(cur_symmetry.get_all_entries(l))
                                    named_tiles[
                                        name
                                        + platform_flavor
                                        + shed_flavor
                                        + "_and"
                                        + platform_flavor_2
                                        + shed_flavor_2
                                    ] = l
                                    named_tiles[
                                        name
                                        + platform_flavor_2
                                        + shed_flavor_2
                                        + "_and"
                                        + platform_flavor
                                        + shed_flavor
                                    ] = l.T


def simple_load(name):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/cns",
        voxel_getter=lambda path=f"station/voxels/cns/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    concourse_components = {"modernnarrow_side", "modernnarrow_side_t"}

    for concourse_flavor, symmetry, ckeeps in [
        ("", BuildingSpriteSheetSymmetrical, set()),
        ("_side", BuildingSpriteSheetSymmetricalX, {"modernnarrow_side"}),
        ("_side_d", BuildingSpriteSheetSymmetrical, {"modernnarrow_side", "modernnarrow_side_t"}),
    ]:
        v2 = v.discard_layers(tuple(sorted(tuple(concourse_components - ckeeps))), "subset" + concourse_flavor)
        v2.in_place_subset(symmetry.render_indices())

        sprite = symmetry.create_variants(v2.spritesheet())
        ps = AParentSprite(sprite, (16, 16, platform_height), (0, 0, 0))
        named_ps[name + concourse_flavor] = ps

        groundsprite = gray_ps
        var = symmetry.get_all_variants(ALayout([groundsprite], [ps], False, notes={"concourse"}))
        l = symmetry.create_variants(var)
        entries.extend(symmetry.get_all_entries(l))
        named_tiles[name + concourse_flavor] = l

        if concourse_flavor != "":
            for shed_flavor, _, _, _, buildable in shed_meta:
                if shed_flavor == "" or not buildable:
                    continue
                shed = named_ps["cns_cut" + shed_flavor]
                for l, needs_symmetrical, extra_suffix in [([shed], False, ""), ([shed, shed.T], True, "_d")]:
                    if needs_symmetrical:
                        if concourse_flavor.endswith("_d"):
                            cur_sym = symmetry
                        else:
                            continue
                    else:
                        cur_sym = BuildingSpriteSheetSymmetricalX
                    var = cur_sym.get_all_variants(ALayout([groundsprite], l + [ps], False, notes={"concourse"}))
                    l = cur_sym.create_variants(var)
                    entries.extend(cur_sym.get_all_entries(l))
                    named_tiles[name + concourse_flavor + shed_flavor + extra_suffix] = l


entries = []
named_ps = AttrDict()
named_tiles = AttrDict()

quickload("cns")
simple_load("concourse")

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
        Demo("Platform", [[cns], [cns_d], [cns.T]]),
        Demo("Platform with concrete grounds", [[cns_side], [cns_d], [cns_side.T]]),
        Demo("Platform with shed", [[cns_shed], [cns_shed_d], [cns_shed.T]]),
    ],
)
