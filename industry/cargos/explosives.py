import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x17,
    b"BOOM",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    weight=4,
    units_text=CargoUnit.CRATE,
)
