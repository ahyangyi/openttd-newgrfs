import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0C,
    b"PAPR",
    grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=12,
    single_penalty_length=60,
    base_price=143,
)
