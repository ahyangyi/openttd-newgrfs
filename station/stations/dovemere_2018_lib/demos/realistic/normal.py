from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import roadstops
from station.stations.dovemere_2018_lib.objects import objects

normal_demo = Demo(
    semitraversable.demo_1(5, 7), "5×7 station layout (1 tile ≈ 40m)", remap=get_1cc_remap(CompanyColour.WHITE)
)
