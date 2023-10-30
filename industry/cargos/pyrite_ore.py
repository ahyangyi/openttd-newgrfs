import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x2A,
    b"PORE",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
