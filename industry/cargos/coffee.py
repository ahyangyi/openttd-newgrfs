import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x14,
    b"JAVA",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.BAG,
    is_freight=1,
    penalty_lowerbound=0,
    single_penalty_length=26,
    base_price=173,
)
