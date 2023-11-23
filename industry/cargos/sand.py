import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x37,
    b"SAND",
    grf.CargoClass.BULK,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=64,
    single_penalty_length=255,
    base_price=93,
)
