import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x28,
    b"PHOS",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
