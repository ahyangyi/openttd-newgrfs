import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1D,
    b"GOLD",
    grf.CargoClass.ARMOURED,
    weight=8,
    units_text=CargoUnit.BAG,
)
