from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import platform, platform_s, concourse_tile
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour
from station.stations.dovemere_2018_lib.flexible_stations import semitraversable
from .utils import h_merge

row_4 = h_merge(
    [semitraversable.cb14b.demo(i, 4, semitraversable.cb24_1) for i in range(1, 5)],
    [[concourse_tile], [platform_s], [platform_s.T], [concourse_tile]],
)
v_sep = [[concourse_tile] * len(row_4[0])] * 2
row_5 = h_merge(
    [semitraversable.cb14b.demo(i, 5, semitraversable.cb24_1) for i in range(1, 5)],
    [[concourse_tile], [platform_s], [platform], [platform_s.T], [concourse_tile]],
)
row_6 = h_merge(
    [semitraversable.cb14b.demo(i, 6, semitraversable.cb24_1) for i in range(1, 5)],
    [[concourse_tile], [platform_s], [platform_s.T], [platform_s], [platform_s.T], [concourse_tile]],
)
row_7 = h_merge(
    [semitraversable.cb14b.demo(i, 7, semitraversable.cb24_1) for i in range(1, 5)],
    [[concourse_tile], [platform_s], [platform], [platform], [platform], [platform_s.T], [concourse_tile]],
)

semi_np_auto_demo = Demo(
    "Semitraversable automatic stations (no platform)",
    row_4 + v_sep + row_5 + v_sep + row_6 + v_sep + row_7,
    remap=get_1cc_remap(CompanyColour.BLUE),
)
