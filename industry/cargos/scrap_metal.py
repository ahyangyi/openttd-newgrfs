import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x35, b"SCMT", grf.CargoClass.BULK | grf.CargoClass.NON_POURABLE)
