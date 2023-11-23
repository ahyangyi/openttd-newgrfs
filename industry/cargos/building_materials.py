import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x11,
    b"BDMT",
    grf.CargoClass.BULK | grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.CRATE,
    is_freight=1,
    penalty_lowerbound=12,
    single_penalty_length=255,
    base_price=133,
)
