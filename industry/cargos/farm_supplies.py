import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x18, b"FMSP", grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS)
