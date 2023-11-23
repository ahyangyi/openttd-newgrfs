import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0A,
    b"DIAM",
    grf.CargoClass.ARMOURED,
    weight=2,
    units_of_cargo=CargoUnit.BAG,
    is_freight=1,
    penalty_lowerbound=30,
    single_penalty_length=255,
    base_price=162,
)
