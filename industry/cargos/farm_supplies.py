import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x18,
    b"FMSP",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    weight=10,
    units_of_cargo=CargoUnit.CRATE,
    is_freight=1,
    penalty_lowerbound=2,
    single_penalty_length=32,
    base_price=170,
)
