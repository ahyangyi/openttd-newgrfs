import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x2F, b"VALU", grf.CargoClass.ARMOURED, weight=2)
