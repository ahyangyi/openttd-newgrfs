import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(0x10, b"NH3_", grf.CargoClass.LIQUID | grf.CargoClass.HAZARDOUS, weight=10)
