import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1A,
    b"FISH",
    grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
)
