import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x2B,
    b"RUBR",
    grf.CargoClass.LIQUID,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=10,
    single_penalty_length=36,
    base_price=110,
)
