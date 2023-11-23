import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x16,
    b"ENSP",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.CRATE,
    is_freight=1,
    penalty_lowerbound=2,
    single_penalty_length=32,
    base_price=172,
)
