import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x04,
    b"LVST",
    grf.CargoClass.PIECE_GOODS,
    weight=3,
    units_of_cargo=CargoUnit.ITEM,
    is_freight=1,
    penalty_lowerbound=0,
    single_penalty_length=15,
    base_price=122,
)
