import grf
from station.lib import AStation
from agrf.graphics.voxel import LazyVoxel
from agrf.graphics.spritesheet import LazyAlternativeSprites
from agrf.sprites import number_alternatives


class BuildingSpriteSheet:
    def __init__(self, things):
        self.things = things

    def all(self):
        return self.things

    @property
    def L(self):
        return self.things[0]

    @property
    def R(self):
        return self.things[2]

    @property
    def TL(self):
        return self.things[4]

    @property
    def TR(self):
        return self.things[6]

    def __getitem__(self, index):
        return self.things[index]


def fixup_callback(thing):
    if isinstance(thing, grf.Switch):
        return grf.Switch(
            ranges={(r.low, r.high): fixup_callback(r.ref) for r in thing._ranges},
            default=fixup_callback(thing.default),
            code=thing.code,
        )
    if isinstance(thing, LazyAlternativeSprites):
        return sprites.index(thing)
    return thing


def quickload(name):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    return BuildingSpriteSheet(v.spritesheet())


(
    front_normal,
    front_gate,
    front_gate_extender,
    central,
    central_windowed,
    central_windowed_extender,
    side_a,
    side_b,
    side_c,
    corner,
) = [
    quickload(name)
    for name in [
        "front_normal",
        "front_gate",
        "front_gate_extender",
        "central",
        "central_windowed",
        "central_windowed_extender",
        "side_a",
        "side_b",
        "side_c",
        "corner",
    ]
]

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
    central_windowed[0],
    central_windowed[1],
    central_windowed[2],
    central_windowed[3],
    front_gate_extender[0],
    front_gate_extender[1],
    central_windowed_extender[0],
    central_windowed_extender[1],
    side_a[0],
    side_a[1],
    side_a[2],
    side_a[3],
    side_a[4],
    side_a[5],
    side_a[6],
    side_a[7],
    side_b[0],
    side_b[1],
    side_b[2],
    side_b[3],
    side_b[4],
    side_b[5],
    side_b[6],
    side_b[7],
    side_c[0],
    side_c[1],
    side_c[2],
    side_c[3],
]


def get_back_index(l, r):
    if l + r == 0:
        # FIXME
        return 2
    if l + r == 1:
        return [16, 18][l]
    if l + r == 2:
        return [16, 2, 18][l]

    e = l + r - 3
    c = e // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([16] + [2] * o + [2] + [2] * c + [2] + [2] * o + [18])[l]


def get_left_index(t, d):
    a = [12, 28, 36, 44, 40, 32, 18]
    if t < d:
        return a[min(t, 3)]
    else:
        return a[-1 - min(d, 3)]


left_wall = grf.Switch(
    ranges={
        t: grf.Switch(
            ranges={d: get_left_index(t, d) for d in range(16)},
            default=2,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=2,
    code="var(0x41, shift=12, and=0x0000000f)",
)
right_wall = grf.Switch(
    ranges={
        t: grf.Switch(
            ranges={d: get_left_index(t, d) + 2 for d in range(16)},
            default=2,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=2,
    code="var(0x41, shift=12, and=0x0000000f)",
)


def get_central_index(l, r):
    if l + r == 0:
        return 6
    if l + r == 1:
        return [left_wall, right_wall][l]
    if l + r == 2:
        return [left_wall, 6, right_wall][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([left_wall] + [6] * o + [20] + [26] * c + [22] + [6] * o + [right_wall])[l]


def get_front_index(l, r):
    if l + r == 0:
        # FIXME
        return corner.L
    if l + r == 1:
        return [corner.L, corner.R][l]
    if l + r == 2:
        # FIXME
        return [corner.L, front_normal.L, corner.R][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return (
        [corner.L]
        + [front_normal.L] * o
        + [front_gate.L]
        + [front_gate_extender.L] * c
        + [front_gate.R]
        + [front_normal.L] * o
        + [corner.R]
    )[l]


cb41 = fixup_callback(
    grf.Switch(
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
)

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=sprites,
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
