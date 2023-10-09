import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x21, b"LVST", grf.CargoClass.PIECE_GOODS, weight=3)
