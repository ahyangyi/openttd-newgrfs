from symmetry import (
    BuildingFull,
    BuildingSymmetrical,
    BuildingSymmetricalX,
    BuildingSymmetricalY,
    BuildingRotational,
    BuildingDiagonal,
    BuildingCylindrical,
)


def test_identity():
    symmetries = [
        BuildingFull,
        BuildingSymmetrical,
        BuildingSymmetricalX,
        BuildingSymmetricalY,
        BuildingRotational,
        BuildingDiagonal,
        BuildingCylindrical,
    ]

    for i in range(len(symmetries)):
        for j in range(i + 1, len(symmetries)):
            assert symmetries[i] is not symmetries[j]


def test_is_symmetrical_y():
    assert not BuildingFull.is_symmetrical_y()
    assert BuildingSymmetrical.is_symmetrical_y()
    assert not BuildingSymmetricalX.is_symmetrical_y()
    assert BuildingSymmetricalY.is_symmetrical_y()
    assert not BuildingRotational.is_symmetrical_y()
    assert not BuildingDiagonal.is_symmetrical_y()
    assert BuildingCylindrical.is_symmetrical_y()
