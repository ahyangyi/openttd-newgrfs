from station.lib import AttrDict, ALayout, BuildingSpriteSheetSymmetricalX, BuildingSpriteSheetSymmetrical
from abc import ABC, abstractmethod
from ..misc import track_ground
from ..ground import named_ps as ground_ps

gray_ps = ground_ps.gray

platform_ps = AttrDict(schema=("name", "platform_clas", "rail_facing", "shelter_class", "location"))
concourse_ps = AttrDict(schema=("platform_class", "side"))
platform_tiles = AttrDict(schema=("name", "platform_class", "rail_facing", "shelter_class", "location", "shelter_side"))
two_side_tiles = AttrDict(
    schema=(
        "name",
        "platform_class",
        "rail_facing",
        "shelter_class",
        "platform_class_2",
        "rail_facing_2",
        "shelter_class_2",
    )
)
concourse_tiles = AttrDict(prefix="concourse", schema=("platform_class", "side", "shelter_class", "shelter_side"))
entries = []


class PlatformFamily(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def get_platform_classes(self):
        pass

    @abstractmethod
    def get_shelter_classes(self):
        pass

    @abstractmethod
    def get_sprite(self, location, rail_facing, platform_class, shelter_class):
        pass

    @abstractmethod
    def get_concourse_sprite(self, location, rail_facing, platform_class, shelter_class):
        pass


def register(pf: PlatformFamily):
    platform_classes = pf.get_platform_classes()
    shelter_classes = pf.get_shelter_classes()
    name = pf.name

    for platform_class in ["np", "cut"] + platform_classes:
        for shelter_class in ["", "pillar"] + shelter_classes:
            if (platform_class, shelter_class) == ("np", ""):
                # Don't create the "nothing" tile
                continue

            if platform_class in ["np", "cut"]:
                rail_facings = [""]
            else:
                rail_facings = ["", "side"]

            if shelter_class == "":
                locations = [""]
            elif shelter_class == "pillar":
                locations = ["", "building", "central"]
            else:
                locations = ["", "building", "building_narrow", "building_v", "building_v_narrow"]

            for location in locations:
                for rail_facing in rail_facings:
                    ps = pf.get_sprite(location, rail_facing, platform_class, shelter_class)
                    platform_ps[(name, platform_class, rail_facing, shelter_class, location)] = ps

                    for l, make_symmetrical, shelter_side in [([ps], False, ""), ([ps, ps.T], True, "d")]:
                        if make_symmetrical:
                            cur_symmetry = ps.sprite.symmetry.add_y_symmetry()
                        else:
                            cur_symmetry = ps.sprite.symmetry
                        var = cur_symmetry.get_all_variants(ALayout(track_ground, l, True))
                        l = cur_symmetry.create_variants(var)
                        if platform_class not in ["np", "cut"] and shelter_class != "pillar" and location == "":
                            entries.extend(cur_symmetry.get_all_entries(l))
                        platform_tiles[(name, platform_class, rail_facing, shelter_class, location, shelter_side)] = l

    for platform_class in platform_classes:
        for rail_facing in ["", "side"]:
            for rail_facing_2 in ["", "side"]:
                for shelter_class in [""] + shelter_classes:
                    for shelter_class_2 in [""] + shelter_classes:
                        if (shelter_class == "" or shelter_class_2 == "" or shelter_class == shelter_class_2) and (
                            (rail_facing, shelter_class) < (rail_facing_2, shelter_class_2)
                        ):
                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            cur_symmetry = BuildingSpriteSheetSymmetricalX
                            var = cur_symmetry.get_all_variants(
                                ALayout(
                                    track_ground,
                                    [platform_ps[(name, *suffix, "")], platform_ps[(name, *suffix2, "")].T],
                                    True,
                                )
                            )
                            l = cur_symmetry.create_variants(var)
                            entries.extend(cur_symmetry.get_all_entries(l))
                            # FIXME merge after removing dc()
                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            two_side_tiles[(name, *suffix, *suffix2)] = l
                            two_side_tiles[(name, *suffix2, *suffix)] = l.T

    for platform_class in [""] + platform_classes:
        for side in ["", "d"] if platform_class != "" else [""]:
            ps = pf.get_concourse_sprite(platform_class, side)
            concourse_ps[(platform_class, side)] = ps

            if platform_class == "" or side == "d":
                symmetry = BuildingSpriteSheetSymmetrical
            else:
                symmetry = BuildingSpriteSheetSymmetricalX

            var = symmetry.get_all_variants(ALayout(gray_ps, [ps], False, notes={"concourse"}))
            l = symmetry.create_variants(var)
            entries.extend(symmetry.get_all_entries(l))
            concourse_tiles[(platform_class, side, "", None)] = l

            if platform_class != "":
                for shelter_class in shelter_classes:
                    shelter = platform_ps[(name, "cut", "", shelter_class, "")]
                    for l, needs_symmetrical, shelter_side in [
                        ([shelter], False, ""),
                        ([shelter, shelter.T], True, "d"),
                    ]:
                        if needs_symmetrical:
                            if side == "d":
                                cur_sym = symmetry
                            else:
                                continue
                        else:
                            cur_sym = BuildingSpriteSheetSymmetricalX
                        var = cur_sym.get_all_variants(ALayout(gray_ps, l + [ps], False, notes={"concourse"}))
                        l = cur_sym.create_variants(var)
                        entries.extend(cur_sym.get_all_entries(l))
                        concourse_tiles[(platform_class, side, shelter_class, shelter_side)] = l
