from dataclass import dataclass
from .symmetry import BuildingSymmetricalX, BuildingDiamond, BuildingCylindrical, BuildingDiagonalAlt


@dataclass
class SlopeType:
    slope_type: int


flat = BuildingCylindrical.create_variants(SlopeType(0))
ortho = BuildingSymmetricalX.create_variants(SlopeType(3), SlopeType(9), SlopeType(12), SlopeType(6))
para = BuildingDiamond.create_variants(SlopeType(5), SlopeType(10))
mono = BuildingDiagonalAlt.create_variants(SlopeType(1), SlopeType(2), SlopeType(8), SlopeType(4))
