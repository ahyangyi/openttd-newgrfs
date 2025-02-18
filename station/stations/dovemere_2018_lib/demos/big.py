from station.lib import Demo
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

big_demo = Demo(
    semitraversable.demo_1(7, 10), "7×10 station layout (1 tile ≈ 30m)", remap=get_1cc_remap(CompanyColour.WHITE)
)
big_half_demo = Demo(
    big_demo.tiles[:5], "7×5 half-station layout (1 tile ≈ 30m)", remap=get_1cc_remap(CompanyColour.WHITE)
)
