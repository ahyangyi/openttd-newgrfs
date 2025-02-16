from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

station_building = h_merge([side.side_station_np_demo(i, 1) for i in range(1, 5)], [[concourse_none]])[0]
n = len(station_building)
station_building_2 = h_merge([side.side_station_np_demo(i, 1) for i in [5, 7]], [[concourse_none]])[0]
assert n == len(station_building_2)

side_np_auto_demo = Demo(
    [
        [x.T for x in station_building],
        [cns.T] * n,
        [cns] * n,
        station_building,
        [concourse_none] * n,
        [concourse_none] * n,
        [x.T for x in station_building_2],
        [cns.T] * n,
        [cns] * n,
        station_building_2,
    ],
    "Nontraversable automatic stations (no platform)",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
