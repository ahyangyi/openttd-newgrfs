from typing import List
from dataclasses import dataclass
from station.lib import AttrDict


@dataclass
class PlatformElement:
    name: str
    components: List[str]
    breaks_y_symmetry: bool
    has_platform: bool
    has_shelter: bool


platform_elements = AttrDict(
    {
        x.name: x
        for x in [
            PlatformElement("full", ["ground level"], False),
            PlatformElement("platform", ["ground level - platform"], True),
            PlatformElement("third", ["ground level - third"], True),
            PlatformElement("third_t", ["ground level - third - t"], True),
        ]
    }
)
