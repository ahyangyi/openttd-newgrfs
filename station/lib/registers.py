import grf
from station.lib.parameters import parameter_list


class Registers:
    ZERO = grf.Temp(0)
    CLIMATE_RAIL_OFFSET = grf.Temp(1)
    CLIMATE_OFFSET = grf.Temp(2)
    SNOW = grf.Temp(3)


snow_track = parameter_list.index("SNOW_TRACK")
disable_snow_pred = f"(var(0x7F, param={snow_track}, shift=0, and=0xffffffff))"


code = f"""
TEMP[0x00] = 0
TEMP[0x01] = (26 * ((terrain_type & 0x5) > 0) * ({disable_snow_pred} == 0) + 82 * (max(track_type, 1) - 1)) * (track_type <= 3)
TEMP[0x02] = 569 * ((terrain_type & 0x5) > 0)
TEMP[0x03] = (terrain_type & 0x4) == 0x4
"""
