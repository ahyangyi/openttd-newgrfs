from station.lib import AttrDict, ALayout, BuildingSymmetricalX, BuildingSymmetrical, add_night_masks
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
        "separator",
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

    def make_notes(platform_class, shelter_class="", shelter_class_2=""):
        notes = []
        if platform_class in platform_classes:
            notes.append(platform_class)
        if shelter_class in shelter_classes:
            notes.append(shelter_class)
        if shelter_class_2 in shelter_classes:
            notes.append(shelter_class_2)
        return notes

    for pid, platform_class in enumerate(["np", "cut"] + platform_classes):
        for sid, shelter_class in enumerate(["", "pillar"] + shelter_classes):
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

            for lid, location in enumerate(locations):
                for rid, rail_facing in enumerate(rail_facings):
                    ps = pf.get_sprite(location, rail_facing, platform_class, shelter_class)
                    platform_ps[(name, platform_class, rail_facing, shelter_class, location)] = ps

                    for ssid, (l, make_symmetrical, shelter_side) in enumerate(
                        [([ps], False, ""), ([ps, ps.T], True, "d")]
                    ):
                        if make_symmetrical:
                            cur_symmetry = ps.sprite.symmetry.add_y_symmetry()
                        else:
                            cur_symmetry = ps.sprite.symmetry

                        var = cur_symmetry.get_all_variants(
                            ALayout(track_ground, l, True, notes=make_notes(platform_class, shelter_class))
                        )
                        l = cur_symmetry.create_variants(var)
                        l = l.symmetry_fmap(lambda x: add_night_masks(x))
                        if platform_class not in ["np", "cut"] and shelter_class != "pillar" and location == "":
                            for i, entry in enumerate(cur_symmetry.get_all_entries(l)):
                                entry.id = (
                                    0x7000 + (pid - 2) * 0x200 + sid * 0x40 + rid * 0x20 + ssid * 0x10 + lid * 0x2 + i
                                )
                                entries.append(entry)
                        platform_tiles[(name, platform_class, rail_facing, shelter_class, location, shelter_side)] = l

    for pid, platform_class in enumerate(platform_classes):
        for rid, rail_facing in enumerate(["", "side"]):
            for rid2, rail_facing_2 in enumerate(["", "side"]):
                for sid, shelter_class in enumerate([""] + shelter_classes):
                    for sid2, shelter_class_2 in enumerate([""] if shelter_class == "" else ["", shelter_class]):
                        if (rail_facing, shelter_class) < (rail_facing_2, shelter_class_2):
                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            cur_symmetry = BuildingSymmetricalX

                            var = cur_symmetry.get_all_variants(
                                ALayout(
                                    track_ground,
                                    [platform_ps[(name, *suffix, "")], platform_ps[(name, *suffix2, "")].T],
                                    True,
                                    notes=make_notes(platform_class, shelter_class, shelter_class_2),
                                )
                            )
                            l = cur_symmetry.create_variants(var)
                            l = l.symmetry_fmap(lambda x: add_night_masks(x))

                            for i, entry in enumerate(cur_symmetry.get_all_entries(l)):
                                entry.id = 0x7800 + pid * 0x80 + rid * 0x40 + rid2 * 0x20 + sid * 0x4 + sid2 * 0x2 + i
                                entries.append(entry)

                            suffix = (platform_class, rail_facing, shelter_class)
                            suffix2 = (platform_class, rail_facing_2, shelter_class_2)
                            two_side_tiles[(name, *suffix, "and", *suffix2)] = l
                            two_side_tiles[(name, *suffix2, "and", *suffix)] = l.T

    for pid, platform_class in enumerate(["none"] + platform_classes):
        for ssid, side in enumerate(["", "d"] if platform_class != "none" else [""]):
            ps = pf.get_concourse_sprite(platform_class, side)
            concourse_ps[(platform_class, side)] = ps

            if platform_class == "none" or side == "d":
                symmetry = BuildingSymmetrical
            else:
                symmetry = BuildingSymmetricalX

            var = symmetry.get_all_variants(
                ALayout(gray_ps, [ps], False, notes=["concourse"] + make_notes(platform_class))
            )
            l = symmetry.create_variants(var)
            l = l.symmetry_fmap(lambda x: add_night_masks(x))
            for i, entry in enumerate(symmetry.get_all_entries(l)):
                entry.id = 0x7A00 + pid * 0x4 + ssid * 0x2 + i
                entries.append(entry)
            concourse_tiles[(platform_class, side, "", None)] = l

            if platform_class != "none":
                for sid, shelter_class in enumerate(shelter_classes):
                    shelter = platform_ps[(name, "cut", "", shelter_class, "")]
                    for lid, (l, needs_symmetrical, shelter_side) in enumerate(
                        [([shelter], False, ""), ([shelter, shelter.T], True, "d")]
                    ):
                        if needs_symmetrical:
                            if side == "d":
                                cur_sym = symmetry
                            else:
                                continue
                        else:
                            cur_sym = BuildingSymmetricalX

                        var = cur_sym.get_all_variants(
                            ALayout(
                                gray_ps,
                                l + [ps],
                                False,
                                notes=["concourse"] + make_notes(platform_class, shelter_class),
                            )
                        )
                        l = cur_sym.create_variants(var)
                        l = l.symmetry_fmap(lambda x: add_night_masks(x))
                        for i, entry in enumerate(cur_sym.get_all_entries(l)):
                            entry.id = 0x7B00 + pid * 0x20 + ssid * 0x10 + sid * 0x4 + lid * 0x2 + i
                            entries.append(entry)
                        concourse_tiles[(platform_class, side, shelter_class, shelter_side)] = l
