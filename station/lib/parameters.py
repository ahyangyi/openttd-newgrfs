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
settings = [
    Parameter(
        "NIGHT_MODE",
        0,
        {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"},
        mapping=ParameterMapping(grf_parameter=0xF, first_bit=0, num_bit=3),
    )
]


def make_introduction_year(station_id, mapping):
    settings.append(Parameter(f"{station_id}_INTRODUCTION_YEAR", 0, limits=(0, 9999), mapping=mapping))


def make_colour(station_id, mapping):
    settings.append(Parameter(f"{station_id}_COLOUR", 0, company_colour, option_name="STATION_COLOUR", mapping=mapping))


# E88A9CA: Wuhu (2015)
settings.append(
    Parameter(
        "E88A9CA_ENABLE_TEMPLATE", 1, booldict, mapping=ParameterMapping(grf_parameter=0x0, first_bit=0, num_bit=1)
    )
)
settings.append(
    Parameter(
        "E88A9CA_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=0x1, first_bit=0, num_bit=1)
    )
)
settings.append(
    Parameter(
        "E88A9CA_ENABLE_ROADSTOP", 1, booldict, mapping=ParameterMapping(grf_parameter=0x2, first_bit=0, num_bit=1)
    )
)
make_introduction_year("E88A9CA", mapping=ParameterMapping(grf_parameter=0x3, first_bit=0, num_bit=13))
make_colour("E88A9CA", mapping=ParameterMapping(grf_parameter=0x10, first_bit=0, num_bit=5))

# E88A9C0: Wuhu (1934)
settings.append(
    Parameter(
        "E88A9C0_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=0x5, first_bit=0, num_bit=1)
    )
)
make_introduction_year("E88A9C0", mapping=ParameterMapping(grf_parameter=0x6, first_bit=0, num_bit=13))
make_colour("E88A9C0", mapping=ParameterMapping(grf_parameter=0x11, first_bit=0, num_bit=5))

# E88A9CP: Platforms
settings.append(
    Parameter(
        "E88A9CP_ENABLE_MODULAR", 1, booldict, mapping=ParameterMapping(grf_parameter=0x8, first_bit=0, num_bit=1)
    )
)

settings.append(
    Parameter("PLATFORM_CONCRETE", 1, booldict, mapping=ParameterMapping(grf_parameter=0x9, first_bit=0, num_bit=1))
)
settings.append(
    Parameter("PLATFORM_BRICK", 0, booldict, mapping=ParameterMapping(grf_parameter=0xA, first_bit=0, num_bit=1))
)

settings.append(
    Parameter("SHELTER_SHELTER_1", 0, booldict, mapping=ParameterMapping(grf_parameter=0xB, first_bit=0, num_bit=1))
)
settings.append(
    Parameter("SHELTER_SHELTER_2", 1, booldict, mapping=ParameterMapping(grf_parameter=0xC, first_bit=0, num_bit=1))
)

parameter_list = ParameterList(settings)

station_meta = ["E88A9CA", "E88A9C0"]
station_cb = {}
station_code = {}
for s in station_meta:
    year = parameter_list[f"{s}_INTRODUCTION_YEAR"].code
    station_cb[s] = {"availability": Switch(ranges={0: 0}, default=1, code=f"current_year >= {year}")}

    colour = parameter_list[f"{s}_COLOUR"].code
    station_code[
        s
    ] = f"""
TEMP[0x05] = ({colour} > 0) * ({colour} + 0x306) + ({colour} == 0) * (0x307 + company_colour1)
"""
