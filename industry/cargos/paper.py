import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0C,
    b"PAPR",
    grf.CargoClass.PIECE_GOODS,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=12,
    penalty2=60,
    base_price=143,
)
