import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"FOOD", grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED)
