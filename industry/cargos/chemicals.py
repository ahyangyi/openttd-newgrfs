import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x38,
    b"RFPR",
    grf.CargoClass.LIQUID | grf.CargoClass.PIECE_GOODS | grf.CargoClass.HAZARDOUS,
    weight=19,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=20,
    single_penalty_length=255,
    base_price=115,
)
