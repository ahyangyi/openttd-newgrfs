import grf
from industry.lib.cargo import ACargo

the_cargo = ACargo(
    0x39, b"BEER", grf.CargoClass.EXPRESS | grf.CargoClass.PIECE_GOODS | grf.CargoClass.LIQUID, weight=17
)
