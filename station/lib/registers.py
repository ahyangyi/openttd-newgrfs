import grf
from agrf.lib.building.registers import Registers as AGRFRegisters, code as agrf_code
from station.lib.parameters import parameter_list


class Registers(AGRFRegisters):
    pass


snow_track = parameter_list.index("SNOW_TRACK")
disable_snow_pred = f"(var(0x7F, param={snow_track}, shift=0, and=0xffffffff))"


code = (
    agrf_code
    + f"""
TEMP[0x01] = (26 * ((terrain_type & 0x5) > 0) * ({disable_snow_pred} == 0) + 82 * (max(track_type, 1) - 1)) * (track_type <= 3)
"""
)
