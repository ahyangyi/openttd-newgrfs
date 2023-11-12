import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x11,
    b"BDMT",
    grf.CargoClass.BULK | grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.CRATE,
    penalty1=12,
    penalty2=255,
    base_price=133,
)
