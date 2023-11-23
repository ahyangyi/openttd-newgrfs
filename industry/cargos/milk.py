import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x3A,
    b"MILK",
    grf.CargoClass.EXPRESS | grf.CargoClass.LIQUID | grf.CargoClass.REFRIGERATED,
    weight=18,
    units_of_cargo=CargoUnit.LITRE,
    is_freight=1,
    penalty_lowerbound=0,
    single_penalty_length=16,
    base_price=131,
)
