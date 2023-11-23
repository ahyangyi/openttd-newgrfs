import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0D,
    b"FRUT",
    grf.CargoClass.BULK | grf.CargoClass.REFRIGERATED,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=0,
    single_penalty_length=26,
    base_price=124,
)
