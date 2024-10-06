from symmetry import BuildingSymmetrical, BuildingSymmetricalX, BuildingSymmetricalY


def test_identity():
    symmetries = [BuildingSymmetrical, BuildingSymmetricalX, BuildingSymmetricalY]

    for i in range(len(symmetries)):
        for j in range(i + 1, len(symmetries)):
            assert symmetries[i] is not symmetries[j]
