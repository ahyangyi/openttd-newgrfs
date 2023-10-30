import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1F,
    b"GRAI",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
)
