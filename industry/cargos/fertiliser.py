import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x19,
    b"FERT",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=22,
    single_penalty_length=44,
    base_price=123,
)
