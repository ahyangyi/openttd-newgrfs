import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x35,
    b"SCMT",
    grf.CargoClass.BULK | grf.CargoClass.NON_POURABLE,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=36,
    penalty2=255,
    base_price=107,
)
