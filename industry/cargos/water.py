import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0F,
    b"WATR",
    grf.CargoClass.LIQUID,
    units_text=CargoUnit.LITRE,
    is_freight=1,
    penalty1=20,
    penalty2=80,
    base_price=93,
)
