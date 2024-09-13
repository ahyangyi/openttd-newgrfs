from station.lib import Demo
from station.stations.platforms import named_tiles as platform_tiles, concourse_tiles, cns_shelter_2, concourse
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side
from .utils import h_merge

station_building = h_merge([side.side_station_demo(i, 1) for i in range(1, 5)], [[concourse_tiles.shelter_2.T]])[0]
n = len(station_building)
station_building_2 = h_merge([side.side_station_demo(i, 1) for i in [5, 7]], [[concourse_tiles.shelter_2.T]])[0]
assert n == len(station_building_2)

side_auto_demo = Demo(
    "Nontraversable automatic stations",
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
