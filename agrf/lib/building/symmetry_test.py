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


def test_break_x_symmetry():
    assert BuildingFull.break_x_symmetry() is BuildingFull
    assert BuildingSymmetrical.break_x_symmetry() is BuildingSymmetricalY
    assert BuildingSymmetricalX.break_x_symmetry() is BuildingFull
    assert BuildingSymmetricalY.break_x_symmetry() is BuildingSymmetricalY
    assert BuildingRotational.break_x_symmetry() is BuildingFull
    assert BuildingDiagonal.break_x_symmetry() is BuildingFull
    assert BuildingCylindrical.break_x_symmetry()._symmetry_descriptor == (0, 0, 1, 1, 0, 0, 1, 1)


def test_break_y_symmetry():
    assert BuildingFull.break_y_symmetry() is BuildingFull
    assert BuildingSymmetrical.break_y_symmetry() is BuildingSymmetricalX
    assert BuildingSymmetricalX.break_y_symmetry() is BuildingSymmetricalX
    assert BuildingSymmetricalY.break_y_symmetry() is BuildingFull
    assert BuildingRotational.break_y_symmetry() is BuildingFull
    assert BuildingDiagonal.break_y_symmetry() is BuildingFull
    assert BuildingCylindrical.break_y_symmetry()._symmetry_descriptor == (0, 0, 0, 0, 1, 1, 1, 1)
