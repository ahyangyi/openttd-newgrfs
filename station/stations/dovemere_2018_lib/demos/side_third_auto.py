from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_s, concourse_tile
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side_third
from .utils import h_merge

platform_asym = platform_tiles.cns_side_and_shed

station_building = h_merge([side_third.cb14.demo(i, 1) for i in range(1, 5)], [[platform_asym]])[0]
n = len(station_building)
station_building_2 = h_merge([side_third.cb14.demo(i, 1) for i in [5, 7]], [[platform_asym]])[0]
assert n == len(station_building_2)

side_third_auto_demo = Demo(
    "Traversable automatic stations",
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
