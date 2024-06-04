from station.lib.parameters import parameter_list
from agrf.magic import Switch

common_cb = {"availability": Switch(ranges={0: 0}, default=1, code="current_year > 2005")}
