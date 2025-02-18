from station.lib import (
    AStation,
    AMetaStation,
    BuildingSymmetrical,
    BuildingSymmetricalX,
    BuildingFull,
    Demo,
    AParentSprite,
    AChildSprite,
    Registers,
)
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from .ground import named_ps as ground_ps
from station.stations.platform_lib import (
    PlatformFamily,
    register,
    platform_ps,
    concourse_ps,
    platform_tiles,
    two_side_tiles,
    concourse_tiles,
    entries,
)
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR


gray_ps = ground_ps.gray


platform_height = 4
platform_width = 5
shelter_height = 17
pillar_height = 18
YOFFSET = 0


class CNSPlatformFamily(PlatformFamily):
    def __init__(self):
        self.v = LazyVoxel(
            "cns",
            prefix=".cache/render/station/cns",
            voxel_getter=lambda path="station/voxels/cns/cns.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        self.concourse = LazyVoxel(
            "concourse",
            prefix=".cache/render/station/cns",
            voxel_getter=lambda path="station/voxels/cns/concourse.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        self.snow_sprites = {}

    @property
    def name(self):
        return "cns"

    def get_platform_classes(self):
        return ["concrete", "brick"]

    def get_shelter_classes(self):
        return ["shelter_1", "shelter_2"]

    def _get_snow_sprite(self, location, shelter_class):
        key = location + "_" + shelter_class
        if key in self.snow_sprites:
            return self.snow_sprites[key]

        if location in ["building"]:
            symmetry = BuildingFull
        else:
            symmetry = BuildingSymmetricalX

        s = shelter_class + ("_" if location != "" else "") + location
        skeeps = {s, s + "_snow"}
        v2 = self.v.discard_layers(
            tuple(sorted(tuple(platform_components) + tuple(shelter_components - skeeps))), f"subset_{s}_snow_base"
        )
        v3 = self.v.discard_layers(
            tuple(sorted(tuple(platform_components) + tuple(shelter_components - {s + "_snow"}))),
            f"subset_{s}_snow_only",
        )
        v = v3.compose(v2, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
        v.config["overlap"] = 1.3
        v.config["agrf_childsprite"] = (0, -YOFFSET)
        v.in_place_subset(symmetry.render_indices())
        s = symmetry.create_variants(v.spritesheet())
        self.snow_sprites[key] = AChildSprite(s, (0, 0), flags={"dodraw": Registers.SNOW})

        return self.snow_sprites[key]

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
        v2.config["agrf_manual_crop"] = (0, YOFFSET)
        if location in ["building", "building_narrow"]:
            symmetry = BuildingFull
        else:
            symmetry = BuildingSymmetricalX
        v2.in_place_subset(symmetry.render_indices())
        foundation_height = platform_height if platform_class == "cut" else 0
        sprite = symmetry.create_variants(
            v2.spritesheet(xdiff=16 - platform_width, xspan=platform_width, zdiff=foundation_height)
        )

        height = max((platform_height if platform_class != "" else 0), (shelter_height if shelter_class != "" else 0))
        if shelter_class in ["shelter_1", "shelter_2"]:
            child_sprites = [self._get_snow_sprite(location.replace("_narrow", ""), shelter_class)]

            # XXX Temporarily disable snow sprites until WenSim adds them in CNS
            child_sprites = []
        else:
            child_sprites = []
        return AParentSprite(
            sprite,
            (16, platform_width, height - foundation_height),
            (0, 16 - platform_width, foundation_height),
            child_sprites=child_sprites,
        )

    def get_concourse_sprite(self, platform_class, side):
        if platform_class == "none":
            ckeeps = set()
        elif side == "d":
            ckeeps = {platform_class, platform_class + "_t"}
        else:
            ckeeps = {platform_class}

        if platform_class == "none" or side == "d":
            symmetry = BuildingSymmetrical
        else:
            symmetry = BuildingSymmetricalX

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
    "shelter_1_snow",
    "shelter_1_building_snow",
    "shelter_1_building_v_snow",
    "shelter_2_snow",
    "shelter_2_building_snow",
    "shelter_2_building_v_snow",
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

platform_ps.populate()
concourse_ps.populate()
platform_tiles.populate()
two_side_tiles.populate()
concourse_tiles.populate()

platform_tiles.globalize()
two_side_tiles.globalize()
concourse_tiles.globalize()

station_tiles = []
for i, entry in enumerate(entries):
    enable_if = []
    for platform_class in ["concrete", "brick"]:
        if platform_class in entry.notes:
            enable_if.append(parameter_list[f"PLATFORM_{platform_class.upper()}"])
    for shelter_class in ["shelter_1", "shelter_2"]:
        if shelter_class in entry.notes:
            enable_if.append(parameter_list[f"SHELTER_{shelter_class.upper()}"])
    station_tiles.append(
        AStation(
            id=entry.id,
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
            enable_if=enable_if,
            doc_layout=entry,
        )
    )

the_stations = AMetaStation(
    station_tiles,
    b"\xe8\x8a\x9cP",
    None,
    [
        Demo([[cns_concrete], [cns_concrete_d], [cns_concrete.T]], "Platform"),
        Demo([[cns_concrete_side], [cns_concrete_d], [cns_concrete_side.T]], "Platform with concrete grounds"),
        Demo(
            [[cns_concrete_shelter_1], [cns_concrete_shelter_1_d], [cns_concrete_shelter_1.T]], "Platform with shelter"
        ),
    ],
)
