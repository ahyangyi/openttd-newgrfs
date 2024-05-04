from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable


normal_demo = Demo(
    "5×7 station layout (roughly 1 tile = 40m)",
    semitraversable.cb14a.demo(5, 7, semitraversable.cb24_0),
    remap=get_1cc_remap(CompanyColour.WHITE),
)
