import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x24, b"OIL_", grf.CargoClass.LIQUID, weight=14)
