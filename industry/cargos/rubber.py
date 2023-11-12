import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x2B,
    b"RUBR",
    grf.CargoClass.LIQUID,
    units_text=CargoUnit.LITRE,
    is_freight=1,
    penalty1=10,
    penalty2=36,
    base_price=110,
)
