import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x11, b"BDMT", grf.CargoClass.BULK | grf.CargoClass.PIECE_GOODS)
