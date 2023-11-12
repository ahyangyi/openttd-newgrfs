import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x04,
    b"LVST",
    grf.CargoClass.PIECE_GOODS,
    weight=3,
    units_text=CargoUnit.ITEM,
    is_freight=1,
    penalty1=0,
    penalty2=15,
    base_price=122,
)
