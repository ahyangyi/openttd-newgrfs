import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x06,
    b"WHEA",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=4,
    penalty2=40,
    base_price=112,
)
