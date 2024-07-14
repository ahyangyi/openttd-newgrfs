from typing import List
from dataclasses import dataclass
from station.lib import AttrDict

platform_height = 4


@dataclass
class PlatformSubelement:
    name: str
    components: List[str]
    height: int
    has_platform: bool

    def get_class_variants(self, class_name):
        return PlatformSubelement(
            "_" + class_name + self.name, {x.format(class_name) for x in self.components}, height, has_platform
        )


platform_meta = [
    PlatformSubelement("_np", set(), 0, False),
    PlatformSubelement("_cut", {"cut"}, platform_height, False),
    PlatformSubelement("_platform", {"{}"}, platform_height, True),
    PlatformSubelement("_side", {"{}_side"}, platform_height, True),
]
