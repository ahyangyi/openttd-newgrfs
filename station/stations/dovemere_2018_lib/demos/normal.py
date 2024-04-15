import grf
from station.lib import Demo, LayoutSprite
from station.stations.dovemere_2018_lib.layouts import *
from station.lib.utils import get_1cc_remap
from agrf.graphics.palette import CompanyColour


normal_demo = Demo(
    "Normal 5×7 station layout (roughly 1 grid = 40m)",
    [
        [corner.T, front_gate.T, front_gate_extender.T, front_gate.TR, corner.TR],
        [side_a_n.T, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.TR],
        [side_b_f.T, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.TR],
        [side_c, central_windowed, central_windowed_extender, central_windowed.R, side_c.R],
        [side_b_f, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.R],
        [side_a_n, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.R],
        [corner, front_gate, front_gate_extender, front_gate.R, corner.R],
    ],
    remap=get_1cc_remap(CompanyColour.WHITE),
)

demo_sprites = []
for demo in [normal_demo, normal_demo.M]:
    demo_sprites.append(
        grf.AlternativeSprites(
            *[
                LayoutSprite(demo, 128 * scale, 128 * scale, xofs=0, yofs=-16 * scale, scale=scale, bpp=bpp)
                for scale in [1, 2, 4]
                for bpp in [32]
            ]
        )
    )
demo_layout1 = ALayout(ADefaultGroundSprite(1012), [AParentSprite(demo_sprites[0], (16, 16, 48), (0, 0, 0))], False)
demo_layout2 = ALayout(ADefaultGroundSprite(1011), [AParentSprite(demo_sprites[1], (16, 16, 48), (0, 0, 0))], False)
layouts.append(demo_layout1)
layouts.append(demo_layout2)
