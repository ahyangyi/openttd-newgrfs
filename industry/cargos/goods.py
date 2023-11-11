import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x05,
    b"GOOD",
    grf.CargoClass.EXPRESS,
    capacity_multiplier=0x200,
    weight=8,
    units_text=CargoUnit.CRATE,
)
