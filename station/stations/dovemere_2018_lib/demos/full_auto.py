from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

row_one = [
    tiny,
    platform,
    h_end_gate,
    h_end_gate.R,
    platform,
    h_end_gate,
    h_gate_extender,
    h_end_gate.R,
    platform,
    h_end,
    h_gate,
    h_gate.R,
    h_end.R,
]

row_two = [
    v_end_gate_third_f,
    platform_s.T,
    corner_gate_2_third_f,
    corner_gate_2_third_f.R,
    platform_s.T,
    corner_gate_2_third_f,
    front_gate_extender,
    corner_gate_2_third_f.R,
    platform_s.T,
    corner_2_third_f,
    front_gate,
    front_gate.R,
    corner_2_third_f.R,
]

row_three_centre = [
    v_central,
    platform,
    side_a2_windowed,
    side_a2_windowed.R,
    platform,
    side_a2_windowed,
    central_windowed_extender,
    side_a2_windowed.R,
    platform,
    side_a2,
    central_windowed,
    central_windowed.R,
    side_a2.R,
]

row_three = [
    v_end_gate_third_f,
    platform_s.T,
    corner_gate_third_f,
    corner_gate_third_f.R,
    platform_s.T,
    corner_gate_third_f,
    front_gate_extender,
    corner_gate_third_f.R,
    platform_s.T,
    corner_third_f,
    front_gate,
    front_gate.R,
    corner_third_f.R,
]

row_four_centre = [
    v_central_n,
    platform_s,
    side_a3_windowed_n,
    side_a3_windowed_n.R,
    platform_s,
    side_a3_windowed_n,
    central_windowed_extender,
    side_a3_windowed_n.R,
    platform_s,
    side_a3_n,
    central_windowed,
    central_windowed.R,
    side_a3_n.R,
]

row_four = [
    v_end_gate_third_f,
    platform_s.T,
    corner_gate_third_f,
    corner_gate_third_f.R,
    platform_s.T,
    corner_gate_third_f,
    front_gate_extender,
    corner_gate_third_f.R,
    platform_s.T,
    corner_third_f,
    front_gate,
    front_gate.R,
    corner_third_f.R,
]

row_five_centre = [
    v_central,
    platform,
    side_d,
    side_d.R,
    platform,
    side_d,
    central_windowed_extender,
    side_d.R,
    platform,
    side_b2,
    central_windowed,
    central_windowed.R,
    side_b2.R,
]

row_five_second = [
    v_central,
    platform,
    side_a3_windowed,
    side_a3_windowed.R,
    platform,
    side_a3_windowed,
    central_windowed_extender,
    side_a3_windowed.R,
    platform,
    side_a,
    central_windowed,
    central_windowed.R,
    side_a.R,
]

row_five = [
    v_end_gate_third_f,
    platform_s.T,
    corner_gate_third_f,
    corner_gate_third_f.R,
    platform_s.T,
    corner_gate_third_f,
    front_gate_extender,
    corner_gate_third_f.R,
    platform_s.T,
    corner_third_f,
    front_gate,
    front_gate.R,
    corner_third_f.R,
]

sep = [gray_layout] * 13

full_auto_demo = Demo(
    "Fully traversable automatic stations",
    [
        row_one,
        sep,
        [x.T for x in row_two],
        row_two,
        sep,
        [x.T for x in row_three],
        row_three_centre,
        row_three,
        sep,
        [x.T for x in row_four],
        [x.T for x in row_four_centre],
        row_four_centre,
        row_four,
        sep,
        [x.T for x in row_five],
        [x.T for x in row_five_second],
        row_five_centre,
        row_five_second,
        row_five,
    ],
    remap=get_1cc_remap(CompanyColour.BLUE),
)
