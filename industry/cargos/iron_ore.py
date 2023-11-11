import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x08,
    b"IORE",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
