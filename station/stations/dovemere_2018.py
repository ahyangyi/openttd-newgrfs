import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet
from agrf.sprites import number_alternatives

front_normal = LazyVoxel(
    "front_normal",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018/front_normal.vox",
    load_from="station/files/gorender.json",
)
front_gate = LazyVoxel(
    "front_gate",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018/front_gate.vox",
    load_from="station/files/gorender.json",
)
central = LazyVoxel(
    "central",
    prefix=f"station/voxels/render/dovemere_2018",
    voxel_getter=lambda: f"station/voxels/dovemere_2018/central.vox",
    load_from="station/files/gorender.json",
)
front_gate_flipped = front_gate.flip("flip")
front_normal.render()
front_gate.render()
front_gate_flipped.render()
central.render()

front_normal = front_normal.spritesheet(0, 0)
front_gate = front_gate.spritesheet(0, 0)
front_gate_flipped = front_gate_flipped.spritesheet(0, 0)
central = central.spritesheet(0, 0)

sprites = front_normal[2:] + front_normal + central[:2] + front_gate[2:] + front_gate_flipped[:2]
print(sprites)

cb41 = grf.Switch(
    ranges={
        (0, 1): 0,
        (2, 3): 2,
        (4, 5): grf.Switch(
            ranges={1: 10, 2: 8},
            default=4,
            code="var(0x41, shift=0, and=0x0000000f)",
        ),
        (6, 7): 6,
    },
    default=0,
    code="var(0x41, shift=24, and=0x0000000f)",
)

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=[number_alternatives(sprites[i], i) for i in range(len(sprites))],
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
        "select_sprite_layout": grf.DualCallback(
            default=cb41,
            purchase=cb41,
        ),
    },
)
