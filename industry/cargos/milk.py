import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x3A,
    b"MILK",
    grf.CargoClass.EXPRESS | grf.CargoClass.LIQUID | grf.CargoClass.REFRIGERATED,
    weight=18,
    units_text=CargoUnit.LITRE,
    is_freight=1,
    penalty1=0,
    penalty2=16,
    base_price=131,
)
