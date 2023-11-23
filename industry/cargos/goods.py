import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x05,
    b"GOOD",
    grf.CargoClass.EXPRESS,
    capacity_multiplier=0x200,
    weight=8,
    units_of_cargo=CargoUnit.CRATE,
    is_freight=1,
    penalty_lowerbound=10,
    single_penalty_length=56,
    base_price=163,
)
