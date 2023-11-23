import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x03,
    b"OIL_",
    grf.CargoClass.LIQUID,
    weight=14,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=30,
    single_penalty_length=255,
    base_price=101,
)
