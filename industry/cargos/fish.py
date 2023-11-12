import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x1A,
    b"FISH",
    grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=0,
    penalty2=18,
    base_price=134,
)
