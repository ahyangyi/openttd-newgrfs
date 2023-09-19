import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(b"PASS", grf.CargoClass.PASSENGERS, capacity_multiplier=0x400, weight=1)
