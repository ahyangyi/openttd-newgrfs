from dataclasses import dataclass
from .symmetry import BuildingSymmetricalX, BuildingDiamond, BuildingCylindrical, BuildingDiagonalAlt, BuildingDiagonal


@dataclass
class SlopeType:
    value: int


flat = BuildingCylindrical.create_variants([SlopeType(0)])
ortho = BuildingSymmetricalX.create_variants([SlopeType(3), SlopeType(9), SlopeType(12), SlopeType(6)])
para = BuildingDiamond.create_variants([SlopeType(5), SlopeType(10)])
mono = BuildingDiagonalAlt.create_variants([SlopeType(1), SlopeType(2), SlopeType(8), SlopeType(4)])
tri = BuildingDiagonal.create_variants([SlopeType(7), SlopeType(14), SlopeType(13), SlopeType(11)])
steep = BuildingDiagonal.create_variants([SlopeType(23), SlopeType(30), SlopeType(27), SlopeType(29)])


def make_slopes(sprites, sym):
    ret = {view: {} for view in sym.render_indices()}

    for slopeGroup in [flat, ortho, para, mono, tri, steep]:
        for slopeType in slopeGroup.all_variants:
            for i in sym.render_indices():
                ret[i][slopeType.value] = sprites[slopeType.value].symmetry_index(i)
    return ret
