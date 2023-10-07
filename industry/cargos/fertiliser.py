import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"FERT", grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS)
