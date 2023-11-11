import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0D,
    b"FRUT",
    grf.CargoClass.BULK | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
)
