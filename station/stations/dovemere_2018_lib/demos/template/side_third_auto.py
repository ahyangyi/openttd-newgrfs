from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all, concourse_tiles
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import side_third
from ..utils import h_merge

globalize_all(platform_class="concrete", shelter_class="shelter_2")

station_building = h_merge([side_third.side_third_station_demo(i, 1) for i in range(1, 5)], [[cns_side_and]])[0]
n = len(station_building)
station_building_2 = h_merge([side_third.side_third_station_demo(i, 1) for i in [5, 7]], [[cns_side_and]])[0]
assert n == len(station_building_2)

side_third_auto_demo = Demo(
    [
        [x.T for x in station_building],
        [cns.T] * n,
        [cns] * n,
        station_building,
        [concourse_tiles.none] * n,
        [concourse_tiles.none] * n,
        [x.T for x in station_building_2],
        [cns.T] * n,
        [cns] * n,
        station_building_2,
    ],
    "Traversable automatic stations",
    remap=get_1cc_remap(CompanyColour.BLUE),
)
