from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_s, concourse_tile
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side
from .utils import h_merge

station_building = h_merge([side.cb14_2.demo(i, 1) for i in range(1, 5)], [[concourse_tile]])[0]
n = len(station_building)
station_building_2 = h_merge([side.cb14_2.demo(i, 1) for i in [5, 7]], [[concourse_tile]])[0]
assert n == len(station_building_2)

side_np_auto_demo = Demo(
    "Nontraversable automatic stations (no platform)",
    [
        [x.T for x in station_building],
        [platform_s.T] * n,
        [platform_s] * n,
        station_building,
        [concourse_tile] * n,
        [concourse_tile] * n,
        [x.T for x in station_building_2],
        [platform_s.T] * n,
        [platform_s] * n,
        station_building_2,
    ],
    remap=get_1cc_remap(CompanyColour.BLUE),
)