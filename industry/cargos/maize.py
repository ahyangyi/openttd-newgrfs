import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x23,
    b"MAIZ",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
