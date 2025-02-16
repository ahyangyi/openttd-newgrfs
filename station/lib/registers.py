import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code


class Registers(AGRFRegisters):
    NIGHTGFX = grf.Temp(0x10)
    SNOW_NIGHTGFX = grf.Temp(0x11)


night = f"var(0x7F, param=15, shift=0, and=0x7)"
code = (
    agrf_code
    + f"""
TEMP[0x10] = (({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)
TEMP[0x11] = ((({night} == 0) * var(0x7F, param=0x41, shift=0, and=0xffffffff)) + ({night} == 1)) * ((terrain_type & 0x4) == 0x4)
"""
)
