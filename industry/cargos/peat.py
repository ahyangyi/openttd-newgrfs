import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x27,
    b"PEAT",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
