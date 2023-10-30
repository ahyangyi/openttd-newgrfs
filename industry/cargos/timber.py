import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x2E,
    b"WDPR",
    grf.CargoClass.BULK | grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.TONNE,
)
