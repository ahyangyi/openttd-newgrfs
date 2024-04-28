from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles, platform_s, rail, gray_layout
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()


def make_line(x, a, b, c, d):
    return [x] * 3 + [a] + [b] * 3 + [c] + [d] * 4 + [c.R] + [b.R] * 3 + [a.R] + [x] * 3


c_n = make_line(platform_s, side_c_n, central, central_windowed, central_windowed_extender)
c_f = [x.T for x in c_n]
c_x = make_line(rail, side_c_x, central, central_windowed, central_windowed_extender)

near_lines = [
    c_x,
    c_n,
    c_f,
    c_n,
    c_f,
    c_x,
    c_x,
    c_n,
    make_line(platform_s.T, side_b_f, central, central_windowed, central_windowed_extender),
    make_line(platform_s, side_a_n, central, central_windowed, central_windowed_extender),
    make_line(gray_layout, corner, front_normal, front_gate, front_gate_extender),
]

far_lines = [[el.T for el in line] for line in near_lines[::-1]]

real_yard_demo = Demo(
    "14×22 rail yard, including pass-through tracks", far_lines + near_lines, remap=get_1cc_remap(CompanyColour.WHITE)
)
