import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x19,
    b"FERT",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.TONNE,
)
