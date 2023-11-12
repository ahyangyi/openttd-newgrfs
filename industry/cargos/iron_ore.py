import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x08,
    b"IORE",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=40,
    penalty2=255,
    base_price=90,
)
