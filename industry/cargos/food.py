import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1B,
    b"FOOD",
    grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
)
