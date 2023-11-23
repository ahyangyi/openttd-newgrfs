import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x35,
    b"SCMT",
    grf.CargoClass.BULK | grf.CargoClass.NON_POURABLE,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=36,
    single_penalty_length=255,
    base_price=107,
)
