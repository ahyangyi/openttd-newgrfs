import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x02,
    b"MAIL",
    grf.CargoClass.MAIL,
    capacity_multiplier=0x200,
    weight=4,
    units_text=CargoUnit.BAG,
    is_freight=0,
    penalty1=6,
    penalty2=24,
    base_price=167,
)
