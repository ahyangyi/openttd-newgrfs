import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"FISH", grf.CargoClass.BULK | grf.CargoClass.PIECE_GOODS)
