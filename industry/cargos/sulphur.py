import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x2D,
    b"SULP",
    grf.CargoClass.BULK | grf.CargoClass.LIQUID | grf.CargoClass.COVERED,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=30,
    single_penalty_length=255,
    base_price=105,
)
