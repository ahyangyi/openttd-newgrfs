import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1C,
    b"WOOL",
    grf.CargoClass.PIECE_GOODS | grf.CargoClass.COVERED,
    weight=3,
    units_text=CargoUnit.ITEM,
    is_freight=1,
    penalty1=8,
    penalty2=48,
    base_price=111,
)
