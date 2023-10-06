import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"SULP", grf.CargoClass.BULK | grf.CargoClass.LIQUID | grf.CargoClass.COVERED)
