from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_s, gray_layout, rail
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side_third
from .utils import h_merge

named_tiles.globalize()

station_building = h_merge([side_third.cb14_2.demo(i, 1) for i in range(1, 5)], [rail])[0]
n = len(station_building)
station_building_2 = h_merge([side_third.cb14_2.demo(i, 1) for i in [5, 7]], [rail])[0]
assert n == len(station_building_2)

side_third_np_auto_demo = Demo(
    "Traversable automatic stations",
    [
        [x.T for x in station_building],
        [platform_s.T] * n,
        [platform_s] * n,
        station_building,
        [gray_layout] * n,
        [gray_layout] * n,
        [x.T for x in station_building_2],
        [platform_s.T] * n,
        [platform_s] * n,
        station_building_2,
    ],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
