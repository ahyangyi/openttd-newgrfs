import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x10,
    b"NH3_",
    grf.CargoClass.LIQUID | grf.CargoClass.HAZARDOUS,
    weight=10,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=32,
    single_penalty_length=64,
    base_price=109,
)
