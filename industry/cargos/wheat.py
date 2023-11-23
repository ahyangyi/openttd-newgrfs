import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x06,
    b"WHEA",
    grf.CargoClass.BULK,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=4,
    single_penalty_length=40,
    base_price=112,
)
