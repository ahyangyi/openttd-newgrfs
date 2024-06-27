from typing import List
from dataclasses import dataclass


@dataclass
class GroundFloorElement:
    name: str
    components: List[str]
    breaks_y_symmetry: bool


@dataclass
class GroundFloorStyle:
    name: str
    components: List[GroundFloorElement]
    breaks_y_symmetry: bool
