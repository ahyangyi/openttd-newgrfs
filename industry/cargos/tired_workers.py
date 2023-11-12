import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x3F,
    b"TRWK",
    grf.CargoClass.PASSENGERS,
    capacity_multiplier=0x400,
    weight=1,
    units_text=CargoUnit.PASSENGER,
    is_freight=0,
    penalty1=0,
    penalty2=18,
    base_price=96,
)
