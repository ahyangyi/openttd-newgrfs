from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetFull,
    Demo,
    AParentSprite,
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
            voxel_getter=lambda path="station/voxels/cns/cns.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        self.concourse = LazyVoxel(
            "concourse",
            prefix="station/voxels/render/cns",
            voxel_getter=lambda path="station/voxels/cns/concourse.vox": path,
            load_from="station/files/cns-gorender.json",
        )

    @property
    def name(self):
        return "cns"

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
            if location == "building_narrow":
                skeeps = {shelter_class + "_building", "pillar_building"}
            elif location == "building_v_narrow":
                skeeps = {shelter_class + "_building_v"}
            else:
                skeeps = {shelter_class + ("_" if location != "" else "") + location}
                if platform_class != "" and shelter_class != "pillar" and location == "building":
                    skeeps.add("escalator")
                if platform_class != "" and shelter_class != "pillar" and location == "building_v":
                    skeeps.add("escalator_v")

        v2 = self.v.discard_layers(
            tuple(sorted(tuple(platform_components - pkeeps) + tuple(shelter_components - skeeps))),
            f"subset_{platform_class}_{rail_facing}_{shelter_class}_{location}",
        )
        if location in ["building", "building_narrow"]:
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

    def get_concourse_sprite(self, platform_class, side):
        if platform_class == "":
            ckeeps = set()
        elif side == "d":
            ckeeps = {platform_class, platform_class + "_t"}
        else:
            ckeeps = {platform_class}

        if platform_class == "" or side == "d":
            symmetry = BuildingSpriteSheetSymmetrical
        else:
            symmetry = BuildingSpriteSheetSymmetricalX

        v2 = self.concourse.discard_layers(
            tuple(sorted(tuple(concourse_components - ckeeps))), f"subset_{platform_class}_{side}"
        )
        v2.in_place_subset(symmetry.render_indices())

        sprite = symmetry.create_variants(v2.spritesheet())
        return AParentSprite(sprite, (16, 16, platform_height), (0, 0, 0))


platform_components = {"cut", "concrete", "concrete_side", "brick", "brick_side"}
platform_classes = ["concrete", "brick"]
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
    "escalator",
    "escalator_v",
    "underground_stairs",  # FIXME
}
shelter_classes = ["shelter_1", "shelter_2"]
concourse_components = {f"{c}{postfix}" for c in platform_classes for postfix in ["", "_t"]}


pf = CNSPlatformFamily()
register(pf)

named_tiles.globalize()
station_tiles = []
for i, entry in enumerate(entries):
    station_tiles.append(
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
    )
    entry.station_id = 0xF000 + i

the_stations = AMetaStation(
    station_tiles,
    b"\xe8\x8a\x9cP",
    None,
    entries,
    [
        Demo("Platform", [[cns], [cns_d], [cns.T]]),
        Demo("Platform with concrete grounds", [[cns_side], [cns_d], [cns_side.T]]),
        Demo("Platform with shelter", [[cns_shelter_1], [cns_shelter_1_d], [cns_shelter_1.T]]),
    ],
)
