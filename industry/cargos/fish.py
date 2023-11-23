import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1A,
    b"FISH",
    grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=0,
    single_penalty_length=18,
    base_price=134,
)
