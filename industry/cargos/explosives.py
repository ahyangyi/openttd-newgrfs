import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x17,
    b"BOOM",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    weight=4,
    units_of_cargo=CargoUnit.CRATE,
    is_freight=1,
    penalty_lowerbound=6,
    single_penalty_length=42,
    base_price=158,
)
