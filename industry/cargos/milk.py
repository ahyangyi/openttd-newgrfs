import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x3A,
    b"MILK",
    grf.CargoClass.EXPRESS | grf.CargoClass.LIQUID | grf.CargoClass.REFRIGERATED,
    weight=18,
    units_text=CargoUnit.LITRE,
)
