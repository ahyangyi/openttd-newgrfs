import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x19, b"FERT", grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS)
