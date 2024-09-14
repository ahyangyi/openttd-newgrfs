from station.lib import Demo
from station.stations.dovemere_2018_lib.layouts import named_tiles
from station.stations.platforms import concourse_tiles, cns_brick_shelter_1
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour

named_tiles.globalize()
nt = concourse_tiles.brick_shelter_1

special_demo_sa = Demo(
    "Irregular 7×7 station layout",
    [
        [
            v_end_brick_platform.M,
            v_central_brick_n.M,
            v_central_brick_n.T.M,
            v_central_brick_n.M,
            v_central_brick_n.T.M,
            v_funnel_2.R.M,
            bicorner_2.T.R,
        ],
        [
            nt.T.M,
            cns_brick_shelter_1.M,
            cns_brick_shelter_1.T.M,
            cns_brick_shelter_1.M,
            corner.R.M,
            double_corner_2,
            v_funnel_2.R,
        ],
        [
            nt.T.M,
            cns_brick_shelter_1.M,
            cns_brick_shelter_1.T.M,
            corner.R.M,
            double_corner_2,
            corner.R,
            v_central_brick_n.T,
        ],
        [nt.T.M, cns_brick_shelter_1.M, corner.R.M, double_corner_2, corner.R, cns_brick_shelter_1, v_central_brick_n],
        [
            nt.T.M,
            corner.R.M,
            double_corner_2,
            corner.R,
            cns_brick_shelter_1.T,
            cns_brick_shelter_1.T,
            v_central_brick_n.T,
        ],
        [
            corner_gate.R.M,
            double_corner_2,
            corner.R,
            cns_brick_shelter_1,
            cns_brick_shelter_1,
            cns_brick_shelter_1,
            v_central_brick_n,
        ],
        [front_gate_extender_corner, corner_gate.R, nt.T, nt.T, nt.T, nt.T, v_end_brick_platform],
    ],
    remap=get_1cc_remap(CompanyColour.PURPLE),
    climate="tropical",
    subclimate="desert",
)
