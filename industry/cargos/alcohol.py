import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x39,
    b"BEER",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS | grf.CargoClass.LIQUID,
    weight=17,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=9,
    single_penalty_length=36,
    base_price=166,
)
