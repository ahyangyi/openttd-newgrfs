import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x34,
    b"ZINC",
    grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=12,
    penalty2=255,
    base_price=126,
)
