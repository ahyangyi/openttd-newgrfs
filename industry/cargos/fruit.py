import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x1C, b"FRUT", grf.CargoClass.BULK | grf.CargoClass.REFRIGERATED)
