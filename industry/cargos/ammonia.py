import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"NH3_", grf.CargoClass.LIQUID | grf.CargoClass.HAZARDOUS)
