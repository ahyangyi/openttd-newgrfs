import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x00,
    b"PASS",
    grf.CargoClass.PASSENGERS,
    capacity_multiplier=0x400,
    weight=1,
    units_text=CargoUnit.PASSENGER,
    penalty1=0,
    penalty2=22,
    base_price=46,
)
