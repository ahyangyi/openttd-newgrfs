import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x15, b"DIAM", grf.CargoClass.ARMOURED, weight=2)
