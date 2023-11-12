import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x28,
    b"PHOS",
    grf.CargoClass.BULK,
    units_text=CargoUnit.TONNE,
    is_freight=1,
    penalty1=30,
    penalty2=255,
    base_price=99,
)
