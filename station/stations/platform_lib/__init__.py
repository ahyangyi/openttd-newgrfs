from station.lib import AttrDict
from abc import ABC, abstractmethod

named_ps = AttrDict()
named_tiles = AttrDict()


class PlatformFamily(ABC):
    @abstractmethod
    def get_platform_classes(self):
        pass

    @abstractmethod
    def get_shelter_classes(self):
        pass

    @abstractmethod
    def get_sprite(self, location, rail_facing, platform_class, shelter_class):
        pass


def us(s: str):
    return "_" + s if s != "" else s


def register(pf: PlatformFamily):
    platform_classes = pf.get_platform_classes()
    shelter_classes = pf.get_shelter_classes()
    name = "cns"  # FIXME

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
                locations = ["", "building", "building_v"]

            for location in locations:
                for rail_facing in rail_facings:
                    suffix = f"{us(platform_class)}{us(rail_facing)}{us(shelter_class)}{us(location)}"
                    ps = pf.get_sprite(location, rail_facing, platform_class, shelter_class)
                    named_ps[name + suffix] = ps

                    for l, make_symmetrical, extra_suffix in [([ps], False, ""), ([ps, ps.T], True, "_d")]:
                        if make_symmetrical:
                            cur_symmetry = ps.symmetry.add_y_symmetry()
                        else:
                            cur_symmetry = ps.symmetry
                        var = cur_symmetry.get_all_variants(ALayout([track_ground], l, True))
                        l = cur_symmetry.create_variants(var)
                        # if sbuildable and pbuildable:
                        #     entries.extend(cur_symmetry.get_all_entries(l))
                        # named_tiles[name + suffix + extra_suffix] = l
