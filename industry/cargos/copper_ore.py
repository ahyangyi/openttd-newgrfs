import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x0E,
    b"CORE",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
    penalty1=30,
    penalty2=255,
    base_price=89,
)
