import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0A,
    b"VALU",
    grf.CargoClass.ARMOURED,
    weight=2,
    units_text=CargoUnit.BAG,
    is_freight=1,
    penalty1=1,
    penalty2=48,
    base_price=178,
)
