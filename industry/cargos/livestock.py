import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x21,
    b"LVST",
    grf.CargoClass.PIECE_GOODS,
    weight=3,
    units_text=CargoUnit.ITEM,
)
