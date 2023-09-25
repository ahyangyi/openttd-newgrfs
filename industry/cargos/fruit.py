import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"FRUT", grf.CargoClass.BULK | grf.CargoClass.REFRIGERATED)
