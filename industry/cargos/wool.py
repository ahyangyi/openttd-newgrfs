import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1C,
    b"WOOL",
    grf.CargoClass.PIECE_GOODS | grf.CargoClass.COVERED,
    weight=3,
    units_of_cargo=CargoUnit.ITEM,
    is_freight=1,
    penalty_lowerbound=8,
    single_penalty_length=48,
    base_price=111,
)
