from dataclasses import dataclass
from symmetry import BuildingCylindrical
from agrf.lib.building.slope import make_slopes


@dataclass
class MockObject:
    debug_id: int


def test_cylindrical():
    sprites = [BuildingCylindrical.create_variants([MockObject(i)]) for i in range(32)]
    ret = make_slopes(sprites, BuildingCylindrical)

    assert False
