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
from .misc import track_ground
from station.stations.platform_lib import PlatformFamily, register, named_ps, named_tiles, entries


gray_ps = ground_ps.gray


platform_height = 4
platform_width = 5
shelter_height = 17
pillar_height = 18


class CNSPlatformFamily(PlatformFamily):
    def __init__(self):
        self.v = LazyVoxel(
            "cns",
            prefix="station/voxels/render/cns",
            voxel_getter=lambda path=f"station/voxels/cns/cns.vox": path,
            load_from="station/files/cns-gorender.json",
        )

    def get_platform_classes(self):
        return ["concrete", "brick"]

    def get_shelter_classes(self):
        return ["shelter_1", "shelter_2"]

    def get_sprite(self, location, rail_facing, platform_class, shelter_class):
        if platform_class == "":
            pkeeps = set()
        else:
            pkeeps = {platform_class + ("_side" if rail_facing == "side" else "")}
        if shelter_class == "":
            skeeps = set()
        else:
            skeeps = {shelter_class + ("_" if location != "" else "") + location}

        v2 = self.v.discard_layers(
            tuple(sorted(tuple(platform_components - pkeeps) + tuple(shelter_components - skeeps))),
            f"subset_{platform_class}_{rail_facing}_{shelter_class}_{location}",
        )
        if location == "building":
            symmetry = BuildingSpriteSheetFull
        else:
            symmetry = BuildingSpriteSheetSymmetricalX
        v2.in_place_subset(symmetry.render_indices())
        foundation_height = platform_height if platform_class == "cut" else 0
        sprite = symmetry.create_variants(
            v2.spritesheet(xdiff=16 - platform_width, xspan=platform_width, zdiff=foundation_height * 2)
        )

        height = max((platform_height if platform_class != "" else 0), (shelter_height if shelter_class != "" else 0))
        return AParentSprite(
            sprite, (16, platform_width, height - foundation_height), (0, 16 - platform_width, foundation_height)
        )


platform_components = {"cut", "concrete", "concrete_side", "brick", "brick_side"}
platform_classes = ["concrete", "brick"]
platform_meta = [
    ("_np", "", False, set(), 0),
    ("_cut", "", False, {"cut"}, platform_height),
    ("", "concrete", True, {"concrete"}, platform_height),
    ("_side", "concrete", True, {"concrete_side"}, platform_height),
    ("_brick", "brick", True, {"brick"}, platform_height),
    ("_brick_side", "brick", True, {"brick_side"}, platform_height),
]


shelter_components = {
    "shelter_1",
    "shelter_1_building",
    "shelter_1_building_v",
    "shelter_2",
    "shelter_2_building",
    "shelter_2_building_v",
    "pillar",
    "pillar_building",
    "pillar_central",
}
shelter_classes = ["shelter_1", "shelter_2"]
shelter_meta = [
    ("", "", BuildingSpriteSheetSymmetricalX, set(), 0, True),
    ("_shelter_1", "shelter_1", BuildingSpriteSheetSymmetricalX, {"shelter_1"}, shelter_height, True),
    ("_shelter_1_building", "shelter_1", BuildingSpriteSheetFull, {"shelter_1_building"}, shelter_height, False),
    (
        "_shelter_1_building_v",
        "shelter_1",
        BuildingSpriteSheetSymmetricalX,
        {"shelter_1_building_v"},
        shelter_height,
        False,
    ),
    ("_shelter_2", "shelter_2", BuildingSpriteSheetSymmetricalX, {"shelter_2"}, shelter_height, True),
    ("_shelter_2_building", "shelter_2", BuildingSpriteSheetFull, {"shelter_2_building"}, shelter_height, False),
    (
        "_shelter_2_building_v",
        "shelter_2",
        BuildingSpriteSheetSymmetricalX,
        {"shelter_2_building_v"},
        shelter_height,
        False,
    ),
    ("_pillar", "pillar", BuildingSpriteSheetSymmetricalX, {"pillar"}, pillar_height, False),
    ("_pillar_building", "pillar", BuildingSpriteSheetFull, {"pillar_building"}, pillar_height, False),
    ("_pillar_central", "pillar", BuildingSpriteSheetSymmetricalX, {"pillar_central"}, pillar_height, False),
]


def simple_load(name):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/cns",
        voxel_getter=lambda path=f"station/voxels/cns/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    concourse_components = {f"{c}{postfix}" for c in platform_classes for postfix in ["", "_t"]}

    for concourse_flavor, symmetry, ckeeps in [
        ("", BuildingSpriteSheetSymmetrical, set()),
        ("_side", BuildingSpriteSheetSymmetricalX, {"concrete"}),
        ("_side_d", BuildingSpriteSheetSymmetrical, {"concrete", "concrete_t"}),
        ("_brick_side", BuildingSpriteSheetSymmetricalX, {"brick"}),
        ("_brick_side_d", BuildingSpriteSheetSymmetrical, {"brick", "brick_t"}),
    ]:
        v2 = v.discard_layers(tuple(sorted(tuple(concourse_components - ckeeps))), "subset" + concourse_flavor)
        v2.in_place_subset(symmetry.render_indices())

        sprite = symmetry.create_variants(v2.spritesheet())
        ps = AParentSprite(sprite, (16, 16, platform_height), (0, 0, 0))
        named_ps[name + concourse_flavor] = ps

        var = symmetry.get_all_variants(ALayout([gray_ps], [ps], False, notes={"concourse"}))
        l = symmetry.create_variants(var)
        entries.extend(symmetry.get_all_entries(l))
        named_tiles[name + concourse_flavor] = l

        if concourse_flavor != "":
            for shelter_flavor, _, _, _, _, buildable in shelter_meta:
                if shelter_flavor == "" or not buildable:
                    continue
                shelter = named_ps["cns_cut" + shelter_flavor]
                for l, needs_symmetrical, extra_suffix in [([shelter], False, ""), ([shelter, shelter.T], True, "_d")]:
                    if needs_symmetrical:
                        if concourse_flavor.endswith("_d"):
                            cur_sym = symmetry
                        else:
                            continue
                    else:
                        cur_sym = BuildingSpriteSheetSymmetricalX
                    var = cur_sym.get_all_variants(ALayout([gray_ps], l + [ps], False, notes={"concourse"}))
                    l = cur_sym.create_variants(var)
                    entries.extend(cur_sym.get_all_entries(l))
                    named_tiles[name + concourse_flavor + shelter_flavor + extra_suffix] = l


pf = CNSPlatformFamily()
register(pf)
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
            class_label=b"\xe8\x8a\x9cP",
            cargo_threshold=40,
            non_traversable_tiles=0b00 if entry.traversable else 0b11,
            callbacks={"select_tile_layout": 0},
        )
        for i, entry in enumerate(entries)
    ],
    b"\xe8\x8a\x9cP",
    None,
    entries,
    [
        Demo("Platform", [[cns], [cns_d], [cns.T]]),
        Demo("Platform with concrete grounds", [[cns_side], [cns_d], [cns_side.T]]),
        Demo("Platform with shelter", [[cns_shelter_1], [cns_shelter_1_d], [cns_shelter_1.T]]),
    ],
)
