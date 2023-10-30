import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x14,
    b"CORE",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
