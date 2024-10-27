from dataclasses import dataclass
from symmetry import BuildingCylindrical, BuildingSymmetricalX, BuildingFull
from agrf.lib.building.slope import make_slopes, slope_types


@dataclass
class MockObject:
    debug_id: int


def test_cylindrical():
    sprites = {i: BuildingCylindrical.create_variants([MockObject(i)]) for i in slope_types}
    ret = make_slopes(sprites, BuildingCylindrical)

    for i in slope_types:
        assert ret[0][i] is sprites[i]


def test_x():
    sprites = {i: BuildingSymmetricalX.create_variants([MockObject(i * 4 + j) for j in range(4)]) for i in slope_types}
    ret = make_slopes(sprites, BuildingSymmetricalX)

    for i in slope_types:
        assert ret[0][i] is sprites[i]


def test_full():
    sprites = {i: BuildingFull.create_variants([MockObject(i * 8 + j) for j in range(8)]) for i in slope_types}
    ret = make_slopes(sprites, BuildingFull)

    for i in slope_types:
        assert ret[0][i] is sprites[i]
