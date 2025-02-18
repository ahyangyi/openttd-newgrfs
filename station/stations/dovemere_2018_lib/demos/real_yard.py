from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import globalize_all, track
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

globalize_all(platform_class="concrete", shelter_class="shelter_2")


def make_line(x, a, b, c, d):
    return [x] * 3 + [a] + [b] * 3 + [c] + [d] * 4 + [c.R] + [b.R] * 3 + [a.R] + [x] * 3


c_n = make_line(cns, side_c_n, central_d, central_windowed_d, central_windowed_extender_d)
c_f = [x.T for x in c_n]
c_empty = make_line(track, side_c_empty, central_d, central_windowed_d, central_windowed_extender_d)

near_lines = [
    c_empty,
    c_n,
    c_f,
    c_n,
    c_f,
    c_empty,
    c_empty,
    c_n,
    make_line(cns.T, side_b_f, central_d, central_windowed_d, central_windowed_extender_d),
    make_line(cns, side_a_n, central_d, central_windowed_d, central_windowed_extender_d),
    make_line(concourse.T, corner_platform, front_normal_platform, front_gate_platform, front_gate_extender_platform),
]

far_lines = [[el.T for el in line] for line in near_lines[::-1]]

real_yard_demo = Demo(
    far_lines + near_lines, "14×22 track yard, including pass-through tracks", remap=get_1cc_remap(CompanyColour.WHITE)
)
