from typing import List
from dataclasses import dataclass


@dataclass
class GroundFloorElement:
    name: str
    components: List[str]
    breaks_y_symmetry: bool


ground_floor_elements = [
    GroundFloorElement("full", ["ground level"], False),
    GroundFloorElement("platform", ["ground level - platform"], True),
    GroundFloorElement("third", ["ground level - third"], True),
    GroundFloorElement("third_t", ["ground level - third - t"], True),
]
ground_floor_elements_lookup = {x.name: x for x in ground_floor_elements}


@dataclass
class GroundFloorStyle:
    name: str
    components: List[GroundFloorElement]
    breaks_y_symmetry: bool
