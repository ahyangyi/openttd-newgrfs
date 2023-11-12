import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0B,
    b"FOOD",
    grf.CargoClass.EXPRESS | grf.CargoClass.REFRIGERATED,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=0,
    penalty2=20,
    base_price=168,
)
