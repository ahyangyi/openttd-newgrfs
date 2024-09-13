from station.lib import Demo
from station.stations.platforms import two_side_tiles, cns_shelter_2, concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side_third
from .utils import h_merge

platform_asym = two_side_tiles.cns_concrete_concrete_shelter_2

station_building = h_merge([side_third.side_third_station_demo(i, 1) for i in range(1, 5)], [[platform_asym]])[0]
n = len(station_building)
station_building_2 = h_merge([side_third.side_third_station_demo(i, 1) for i in [5, 7]], [[platform_asym]])[0]
assert n == len(station_building_2)

side_third_auto_demo = Demo(
    "Traversable automatic stations",
    [
        [x.T for x in station_building],
        [cns_shelter_2.T] * n,
        [cns_shelter_2] * n,
        station_building,
        [concourse] * n,
        [concourse] * n,
        [x.T for x in station_building_2],
        [cns_shelter_2.T] * n,
        [cns_shelter_2] * n,
        station_building_2,
    ],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
