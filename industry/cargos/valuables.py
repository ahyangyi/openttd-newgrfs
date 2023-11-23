import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0A,
    b"VALU",
    grf.CargoClass.ARMOURED,
    weight=2,
    units_of_cargo=CargoUnit.BAG,
    is_freight=1,
    penalty_lowerbound=1,
    single_penalty_length=48,
    base_price=178,
)
