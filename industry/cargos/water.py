import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0F,
    b"WATR",
    grf.CargoClass.LIQUID,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=20,
    single_penalty_length=80,
    base_price=93,
)
