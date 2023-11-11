import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0A,
    b"VALU",
    grf.CargoClass.ARMOURED,
    weight=2,
    units_text=CargoUnit.BAG,
)
