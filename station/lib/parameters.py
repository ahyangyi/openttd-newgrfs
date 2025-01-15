from agrf.parameters import Parameter, ParameterList
from agrf.magic import Switch

booldict = {0: "DISABLED", 1: "ENABLED"}
company_colour = {
    0: "PRIMARY",
    1: "DARK_BLUE",
    2: "PALE_GREEN",
    3: "PINK",
    4: "YELLOW",
    5: "RED",
    6: "LIGHT_BLUE",
    7: "GREEN",
    8: "DARK_GREEN",
    9: "BLUE",
    10: "CREAM",
    11: "MAUVE",
    12: "PURPLE",
    13: "ORANGE",
    14: "BROWN",
    15: "GREY",
    16: "WHITE",
}
global_settings = []

station_meta = ["E88A9CA", "E88A9C0"]
station_settings = []
for s in station_meta:
    if s == "E88A9CA":
        station_settings.append(Parameter(f"{s}_ENABLE_TEMPLATE", 1, booldict))
    station_settings.append(Parameter(f"{s}_ENABLE_MODULAR", 1, booldict))
    if s == "E88A9CA":
        station_settings.append(Parameter(f"{s}_ENABLE_ROADSTOP", 1, booldict))
    station_settings.append(Parameter(f"{s}_INTRODUCTION_YEAR", 0, limits=(0, 9999)))
    station_settings.append(Parameter(f"{s}_COLOUR", 0, company_colour, option_name="STATION_COLOUR"))
station_settings.append(Parameter("E88A9CP_ENABLE_MODULAR", 1, booldict))

platform_settings = []
for platform, enabled in [("concrete", True), ("brick", False)]:
    platform_settings.append(Parameter(f"PLATFORM_{platform.upper()}", int(enabled), booldict))

shelter_settings = []
for shelter, enabled in [("shelter_1", False), ("shelter_2", True)]:
    shelter_settings.append(Parameter(f"SHELTER_{shelter.upper()}", int(enabled), booldict))

parameter_list = ParameterList(global_settings + station_settings + platform_settings + shelter_settings)

station_cb = {}
for s in station_meta:
    station_param = parameter_list.index(f"{s}_INTRODUCTION_YEAR")
    station_cb[s] = {
        "availability": Switch(
            ranges={0: 0}, default=1, code=f"current_year >= var(0x7F, param={station_param}, shift=0, and=0xffffffff)"
        )
    }
