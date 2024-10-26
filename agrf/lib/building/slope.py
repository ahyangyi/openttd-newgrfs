from dataclass import dataclass
from .symmetry import BuildingSymmetricalX, BuildingDiamond, BuildingCylindrical, BuildingDiagonalAlt, BuildingDiagonal


@dataclass
class SlopeType:
    slope_type: int


flat = BuildingCylindrical.create_variants(SlopeType(0))
ortho = BuildingSymmetricalX.create_variants(SlopeType(3), SlopeType(9), SlopeType(12), SlopeType(6))
para = BuildingDiamond.create_variants(SlopeType(5), SlopeType(10))
mono = BuildingDiagonalAlt.create_variants(SlopeType(1), SlopeType(2), SlopeType(8), SlopeType(4))
tri = BuildingDiagonal.create_variants(SlopeType(7), SlopeType(14), SlopeType(13), SlopeType(11))
steep = BuildingDiagonal.create_variants(SlopeType(23), SlopeType(30), SlopeType(27), SlopeType(29))
