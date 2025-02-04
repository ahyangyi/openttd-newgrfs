from typing import List
from dataclasses import dataclass
from station.lib import AttrDict


@dataclass
class GroundFloorElement:
    name: str
    components: List[str]
    breaks_y_symmetry: bool


ground_floor_elements = AttrDict(
    {
        x.name: x
        for x in [
            GroundFloorElement("full", ["ground level"], False),
            GroundFloorElement("platform", ["ground level - platform"], True),
            GroundFloorElement("third", ["ground level - third"], True),
            GroundFloorElement("third_t", ["ground level - third - t"], True),
        ]
    }
)


@dataclass
class GroundFloorStyle:
    name: str
    components: List[GroundFloorElement]
    breaks_y_symmetry: bool


ground_floor_styles = AttrDict(
    {
        x.name: x
        for x in [
            GroundFloorStyle("n", [], False),
            GroundFloorStyle("f", [], False),
            GroundFloorStyle("d", [], False),
            GroundFloorStyle("corridor", [ground_floor_elements.third, ground_floor_elements.third_t], False),
            GroundFloorStyle("full", [ground_floor_elements.full], False),
            GroundFloorStyle("platform", [ground_floor_elements.platform], True),
            GroundFloorStyle("third", [ground_floor_elements.third], True),
            GroundFloorStyle("third_t", [ground_floor_elements.third_t], True),
        ]
    }
)
