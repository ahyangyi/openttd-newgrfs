import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x39,
    b"BEER",
    grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS | grf.CargoClass.LIQUID,
    weight=17,
    units_text=CargoUnit.LITRE,
    is_freight=1,
    penalty1=9,
    penalty2=36,
    base_price=166,
)
