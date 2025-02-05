import grf
from agrf.parameters import Parameter, ParameterList
from agrf.magic import Switch
from grf import ParameterMapping

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
global_settings = [
    Parameter(
        "NIGHT_MODE",
        0,
        {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"},
        mapping=ParameterMapping(grf_parameter=15, first_bit=0, num_bit=3),
    )
]

station_settings = []


def make_introduction_year(station_id, mapping):
    station_settings.append(Parameter(f"{station_id}_INTRODUCTION_YEAR", 0, limits=(0, 9999), mapping=mapping))


def make_colour(station_id, mapping):
    station_settings.append(
        Parameter(f"{station_id}_COLOUR", 0, company_colour, option_name="STATION_COLOUR", mapping=mapping)
    )


# E88A9CA: Wuhu (2015)
station_settings.append(
    Parameter("E88A9CA_ENABLE_TEMPLATE", 1, booldict, mapping=ParameterMapping(grf_parameter=0, first_bit=0, num_bit=1))
)
station_settings.append(
    Parameter("E88A9CA_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=1, first_bit=0, num_bit=1))
)
station_settings.append(
    Parameter("E88A9CA_ENABLE_ROADSTOP", 1, booldict, mapping=ParameterMapping(grf_parameter=2, first_bit=0, num_bit=1))
)
make_introduction_year("E88A9CA", mapping=ParameterMapping(grf_parameter=3, first_bit=0, num_bit=13))
make_colour("E88A9CA", mapping=ParameterMapping(grf_parameter=16, first_bit=0, num_bit=5))

# E88A9C0: Wuhu (1934)
station_settings.append(
    Parameter("E88A9C0_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=5, first_bit=0, num_bit=1))
)
make_introduction_year("E88A9C0", mapping=ParameterMapping(grf_parameter=6, first_bit=0, num_bit=13))
make_colour("E88A9C0", mapping=ParameterMapping(grf_parameter=17, first_bit=0, num_bit=5))

# E88A9CP: Platforms
station_settings.append(
    Parameter("E88A9CP_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=8, first_bit=0, num_bit=1))
)

platform_settings = []
platform_settings.append(
    Parameter(f"PLATFORM_CONCRETE", 1, booldict, mapping=ParameterMapping(grf_parameter=9, first_bit=0, num_bit=1))
)
platform_settings.append(
    Parameter(f"PLATFORM_BRICK", 0, booldict, mapping=ParameterMapping(grf_parameter=0xA, first_bit=0, num_bit=1))
)

shelter_settings = []
shelter_settings.append(
    Parameter(f"SHELTER_SHELTER_1", 0, booldict, mapping=ParameterMapping(grf_parameter=0xB, first_bit=0, num_bit=1))
)
shelter_settings.append(
    Parameter(f"SHELTER_SHELTER_2", 1, booldict, mapping=ParameterMapping(grf_parameter=0xC, first_bit=0, num_bit=1))
)

parameter_list = ParameterList(global_settings + station_settings + platform_settings + shelter_settings)

station_meta = ["E88A9CA", "E88A9C0"]
station_cb = {}
station_code = {}
for i, s in enumerate(station_meta):
    year = parameter_list[f"{s}_INTRODUCTION_YEAR"].code
    station_cb[s] = {"availability": Switch(ranges={0: 0}, default=1, code=f"current_year >= {year}")}

    colour = parameter_list[f"{s}_COLOUR"].code
    station_code[
        s
    ] = f"""
TEMP[0x05] = ({colour} > 0) * ({colour} + 0x306) + ({colour} == 0) * (0x307 + company_colour1)
"""
