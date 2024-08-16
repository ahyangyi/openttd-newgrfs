from agrf.parameters import Parameter, ParameterList
from agrf.magic import Switch

global_settings = [Parameter("INTRODUCTION_YEAR", 0, {0: "DISABLED", 1: "ENABLED"})]

station_meta = [("E88A9CA", 2005), ("E88A9C0", 1911)]
station_settings = []
for s, year in station_meta:
    station_settings.append(Parameter(f"{s}_INTRODUCTION_YEAR", year, limits=(0, 9999)))

parameter_list = ParameterList(global_settings + station_settings)

station_cb = {}
for s, _ in station_meta:
    enabled = parameter_list.index("INTRODUCTION_YEAR")
    station_param = parameter_list.index(f"{s}_INTRODUCTION_YEAR")
    station_cb[s] = {
        "availability": Switch(
            ranges={0: 0},
            default=1,
            code=f"current_year > (var(0x7F, param={enabled}, shift=0, and=0xffffffff) * var(0x7F, param={station_param}, shift=0, and=0xffffffff))",
        )
    }
