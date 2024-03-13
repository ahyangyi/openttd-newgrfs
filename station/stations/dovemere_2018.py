import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel
from agrf.sprites import number_alternatives

front_normal, front_gate, front_gate_extender, central, central_windowed, central_windowed_extender, side_a, corner = [
    LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    for name in [
        "front_normal",
        "front_gate",
        "front_gate_extender",
        "central",
        "central_windowed",
        "central_windowed_extender",
        "side_a",
        "corner",
    ]
]

front_normal.render()
front_gate.render()
front_gate_extender.render()
central.render()
central_windowed.render()
central_windowed_extender.render()
side_a.render()
corner.render()

front_normal = front_normal.spritesheet(0, 0)
front_gate = front_gate.spritesheet(0, 0)
front_gate_extender = front_gate_extender.spritesheet(0, 0)
central = central.spritesheet(0, 0)
central_windowed = central_windowed.spritesheet(0, 0)
central_windowed_extender = central_windowed_extender.spritesheet(0, 0)
side_a = side_a.spritesheet(0, 0)
corner = corner.spritesheet(0, 0)

sprites = [
    front_normal[0],
    front_normal[1],
    front_normal[4],
    front_normal[5],
    front_normal[0],
    front_normal[1],
    central[0],
    central[1],
    front_gate[0],
    front_gate[1],
    front_gate[2],
    front_gate[3],
    corner[0],
    corner[1],
    corner[2],
    corner[3],
    corner[4],
    corner[5],
    corner[6],
    corner[7],
    central_windowed[2],
    central_windowed[3],
    central_windowed[0],
    central_windowed[1],
    front_gate_extender[0],
    front_gate_extender[1],
    central_windowed_extender[2],
    central_windowed_extender[3],
    side_a[0],
    side_a[1],
    side_a[2],
    side_a[3],
]


def get_back_index(l, r):
    if l + r == 0:
        # FIXME
        return 2
    if l + r == 1:
        return [18, 16][l]
    if l + r == 2:
        return [18, 2, 16][l]

    e = l + r - 3
    c = e // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([18] + [2] * o + [2] + [2] * c + [2] + [2] * o + [16])[l]


def get_central_index(l, r):
    if l + r == 0:
        return 6
    if l + r == 1:
        return [28, 30][l]
    if l + r == 2:
        return [28, 6, 30][l]

    e = l + r - 3
    c = e // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([28] + [6] * o + [22] + [26] * c + [20] + [6] * o + [30])[l]


def get_front_index(l, r):
    if l + r == 0:
        # FIXME
        return 4
    if l + r == 1:
        return [12, 14][l]
    if l + r == 2:
        # FIXME
        return [12, 4, 14][l]

    e = l + r - 3
    c = e // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([12] + [4] * o + [8] + [24] * c + [10] + [4] * o + [14])[l]


cb41 = grf.Switch(
    ranges={
        (0, 1): 0,
        (2, 3): grf.Switch(
            ranges={
                l: grf.Switch(
                    ranges={r: get_back_index(l, r) for r in range(16)},
                    default=2,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=2,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (4, 5): grf.Switch(
            ranges={
                l: grf.Switch(
                    ranges={r: get_front_index(l, r) for r in range(16)},
                    default=4,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=4,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (6, 7): grf.Switch(
            ranges={
                l: grf.Switch(
                    ranges={r: get_central_index(l, r) for r in range(16)},
                    default=6,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=6,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
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
