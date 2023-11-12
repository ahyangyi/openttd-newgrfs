import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x33,
    b"WRKR",
    grf.CargoClass.PASSENGERS,
    capacity_multiplier=0x400,
    weight=1,
    units_text=CargoUnit.PASSENGER,
    is_freight=0,
    penalty1=0,
    penalty2=16,
    base_price=104,
)
