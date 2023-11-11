import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x03,
    b"OIL_",
    grf.CargoClass.LIQUID,
    weight=14,
    units_text=CargoUnit.LITRE,
)
