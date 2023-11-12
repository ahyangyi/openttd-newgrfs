import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0D,
    b"FRUT",
    grf.CargoClass.BULK | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=0,
    penalty2=26,
    base_price=124,
)
