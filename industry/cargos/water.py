import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0F,
    b"WATR",
    grf.CargoClass.LIQUID,
    units_text=CargoUnit.LITRE,
)
