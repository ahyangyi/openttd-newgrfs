import grf
from industry.lib.cargo import ACargo, CargoUnit

the_cargo = ACargo(
    0x29,
    b"POTA",
    grf.CargoClass.BULK | grf.CargoClass.COVERED,
    units_text=CargoUnit.TONNE,
)
