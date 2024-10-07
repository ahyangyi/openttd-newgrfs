from station.lib import Demo
from station.lib.utils import get_1cc_remap
from station.stations.platforms import two_side_tiles
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.layouts import globalize_all, concourse_tiles
from station.stations.dovemere_2018_lib.flexible_stations import traversable
from .utils import h_merge

full_auto_demo = Demo(
    "Fully traversable automatic stations",
    traversable.demo_1(2, 2),
    remap=get_1cc_remap(CompanyColour.BLUE),
)
