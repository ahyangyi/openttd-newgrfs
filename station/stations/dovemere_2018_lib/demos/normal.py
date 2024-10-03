from station.lib import Demo
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from station.stations.dovemere_2018_lib.roadstops import roadstops
from station.stations.dovemere_2018_lib.objects import objects

stop1 = roadstops[0].doc_layout.lower_tile()
stop2 = roadstops[4].doc_layout.lower_tile()
stop3 = roadstops[12].doc_layout.lower_tile()
roadstops = [[stop1, stop2, stop3, stop2.R, stop1]]
west_square = [[objects[0].doc_layout.lower_tile()] * 5, [objects[0].doc_layout.lower_tile()] * 5]


normal_demo = Demo(
    "5×7 station layout (roughly 1 tile = 40m)",
    semitraversable.demo_1(5, 7) + roadstops + west_square,
    remap=get_1cc_remap(CompanyColour.WHITE),
)
