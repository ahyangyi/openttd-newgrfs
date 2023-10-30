import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x25,
    b"PAPR",
    grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.TONNE,
)
