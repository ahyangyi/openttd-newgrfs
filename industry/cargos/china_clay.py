import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x12, b"KAOL", grf.CargoClass.BULK | grf.CargoClass.LIQUID | grf.CargoClass.COVERED)
