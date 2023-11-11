import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x06,
    b"WHEA",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
