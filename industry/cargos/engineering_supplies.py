import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x16,
    b"ENSP",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.CRATE,
)
