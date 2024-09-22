from station.lib import Demo
from station.stations.platforms import cns_shelter_2_d, cns_shelter_2, concourse, concourse_tiles
from station.stations.dovemere_2018_lib.layouts import named_tiles
from station.stations.misc import default
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = concourse_tiles.shelter_2

special_demo_cp = Demo(
    "Irregular 7×7 station layout",
    [
        [h_end_corridor, tee.T, h_normal_corridor, turn.T.R, default, default, default],
        [
            cns_shelter_2,
            v_central_shelter_2_n,
            cns_shelter_2,
            v_central_shelter_2_n,
            cns_shelter_2_d,
            cns_shelter_2_d,
            cns_shelter_2_d,
        ],
        [
            cns_shelter_2.T,
            v_central_shelter_2_n.T,
            cns_shelter_2.T,
            v_central_shelter_2_n.T,
            cns_shelter_2_d,
            cns_shelter_2_d,
            cns_shelter_2_d,
        ],
        [
            cns_shelter_2,
            v_central_shelter_2_n,
            cns_shelter_2,
            v_central_shelter_2_n,
            corner.T,
            front_normal.T,
            corner.T.R,
        ],
        [
            nt.T,
            v_end_shelter_2_platform,
            nt.T,
            turn,
            double_inner_corner,
            central_windowed_extender_d,
            side_a2_windowed_shelter_2_d.R,
        ],
        [concourse, concourse, concourse, concourse, v_funnel, front_normal, corner.R],
        [default, default, default, default, v_end_gate, default, default],
    ],
    remap=get_1cc_remap(CompanyColour.CREAM),
    climate="toyland",
)
