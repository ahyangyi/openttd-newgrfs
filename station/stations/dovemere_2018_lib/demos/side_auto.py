from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform_n, concourse_tile
from station.stations.platforms import named_tiles as platform_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side
from .utils import h_merge

station_building = h_merge(
    [side.side_station_demo(i, 1) for i in range(1, 5)], [[platform_tiles.concourse_side_shelter_1.T]]
)[0]
n = len(station_building)
station_building_2 = h_merge(
    [side.side_station_demo(i, 1) for i in [5, 7]], [[platform_tiles.concourse_side_shelter_1.T]]
)[0]
assert n == len(station_building_2)

side_auto_demo = Demo(
    "Nontraversable automatic stations",
    [
        [x.T for x in station_building],
        [platform_n.T] * n,
        [platform_n] * n,
        station_building,
        [concourse_tile] * n,
        [concourse_tile] * n,
        [x.T for x in station_building_2],
        [platform_n.T] * n,
        [platform_n] * n,
        station_building_2,
    ],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
