import grf


class Registers:
    ZERO = grf.Temp(0)
    CLIMATE_RAIL_OFFSET = grf.Temp(1)


code = """
TEMP[0x00] = 0
TEMP[0x01] = 26 * ((terrain_type & 0x5) > 0) + 82 * (max(track_type, 1) - 1)
"""
