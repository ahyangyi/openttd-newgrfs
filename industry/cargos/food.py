import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x1B, b"FOOD", grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED)
