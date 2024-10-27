from dataclasses import dataclass
from symmetry import BuildingCylindrical
from agrf.lib.building.slope import make_slopes

indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 23, 27, 29]


@dataclass
class MockObject:
    debug_id: int


def test_cylindrical():
    sprites = {i: BuildingCylindrical.create_variants([MockObject(i)]) for i in indices}
    ret = make_slopes(sprites, BuildingCylindrical)

    for i in indices:
        assert ret[0][i] is sprites[i]
