from station.lib.parameters import parameter_list
from agrf.magic import Switch

enabled = parameter_list.index("INTRODUCTION_YEAR")
station_param = parameter_list.index("E88A9CA_INTRODUCTION_YEAR")
common_cb = {
    "availability": Switch(
        ranges={0: 0},
        default=1,
        code=f"current_year > (var(0x7F, param={enabled}, shift=0, and=0xffffffff) * var(0x7F, param={station_param}, shift=0, and=0xffffffff))",
    )
}
