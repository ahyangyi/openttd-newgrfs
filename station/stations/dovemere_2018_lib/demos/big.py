from station.lib import Demo
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

big_demo = Demo(
    "8×12 station layout (roughly 1 tile = 25m)",
    semitraversable.cb14a.demo(8, 12, semitraversable.cb24_0),
    remap=get_1cc_remap(CompanyColour.WHITE),
)
big_half_demo = Demo(
    "8×6 half-station layout (roughly 1 tile = 25m)", big_demo.tiles[:6], remap=get_1cc_remap(CompanyColour.WHITE)
)
