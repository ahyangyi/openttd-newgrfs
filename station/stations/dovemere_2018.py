import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet
from agrf.sprites import number_alternatives

vox = LazyVoxel(
    "dovemere_2018",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018.vox",
    load_from="station/files/gorender.json",
)
vox.render()
voxels = [LazySpriteSheet([vox], [(0, i)]) for i in range(4)]

cb41 = grf.Switch(
    ranges={i: i * 2 for i in range(16)},
    default=0,
    code="var(0x41, shift=0, and=0x0000000f)",
)

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=[number_alternatives(voxels[(i + 2) % 4].spritesheet(0, 0)[0], i) for i in range(100)],
    class_label=b"DM18",
    cargo_threshold=40,
    callbacks={
        "select_tile_layout": grf.PurchaseCallback(
            purchase=grf.Switch(
                ranges={
                    (2, 15): grf.Switch(
                        ranges={0: 2},
                        default=grf.Switch(
                            ranges={0: 4},
                            default=6,
                            code="(extra_callback_info1 >> 12) & 0xf",
                        ),
                        code="(extra_callback_info1 >> 8) & 0xf",
                    )
                },
                default=0,
                code="(extra_callback_info1 >> 20) & 0xf",
            ),
        ),
        # "select_sprite_layout": grf.DualCallback(
        #    default=cb41,
        #    purchase=cb41,
        # ),
    },
)
