import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"ENSP", grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS)
