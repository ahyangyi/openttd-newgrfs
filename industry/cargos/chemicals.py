import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(
    0x38, b"RFPR", grf.CargoClass.LIQUID | grf.CargoClass.PIECE_GOODS | grf.CargoClass.HAZARDOUS, weight=19
)
