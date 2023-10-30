import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x22,
    b"MAIL",
    grf.CargoClass.MAIL,
    capacity_multiplier=0x200,
    weight=4,
    units_text=CargoUnit.BAG,
)
