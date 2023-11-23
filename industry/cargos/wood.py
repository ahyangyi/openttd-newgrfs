import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x07,
    b"WOOD",
    grf.CargoClass.PIECE_GOODS,
    units_of_cargo=CargoUnit.TONNE,
    is_freight=1,
    penalty_lowerbound=24,
    single_penalty_length=255,
    base_price=104,
)
