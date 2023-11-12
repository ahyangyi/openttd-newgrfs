import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x03,
    b"OIL_",
    grf.CargoClass.LIQUID,
    weight=14,
    units_text=CargoUnit.LITRE,
    is_freight=1,
    penalty1=30,
    penalty2=255,
    base_price=101,
)
