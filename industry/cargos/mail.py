import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo("MAIL", grf.CargoClass.MAIL, capacity_multiplier=0x200, weight=4)
