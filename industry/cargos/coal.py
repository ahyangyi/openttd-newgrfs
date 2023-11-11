import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x01,
    b"COAL",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
