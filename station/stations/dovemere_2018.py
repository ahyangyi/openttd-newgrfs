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

    def __getitem__(self, index):
        return type(self)([self.things[index ^ x] for x in range(len(self.things))])

    @property
    def sprite(self):
        return self.things[0]


class BuildingSpriteSheetFull(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetFull(things)

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]

    @property
    def TL(self):
        return self[4]

    @property
    def TR(self):
        return self[6]


class BuildingSpriteSheetSymmetricalX(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetricalX([things[0], things[1], things[4], things[5]])

    @property
    def C(self):
        return self

    @property
    def T(self):
        return self[2]


class BuildingSpriteSheetSymmetricalY(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetricalY([things[0], things[1], things[2], things[3]])

    @property
    def L(self):
        return self

    @property
    def R(self):
        return self[2]


class BuildingSpriteSheetSymmetrical(BuildingSpriteSheet):
    def __init__(self, things):
        super().__init__(things)

    @staticmethod
    def from_complete_list(things):
        return BuildingSpriteSheetSymmetrical([things[0], things[1]])


def fixup_callback(thing):
    if isinstance(thing, grf.Switch):
        return grf.Switch(
            ranges={(r.low, r.high): fixup_callback(r.ref) for r in thing._ranges},
            default=fixup_callback(thing.default),
            code=thing.code,
        )
    if isinstance(thing, BuildingSpriteSheet):
        return sprites.index(thing.sprite)
    return thing


def quickload(name, type):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    ret = type.from_complete_list(v.spritesheet())
    sprites.extend(ret.all())
    return ret


sprites = []
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
    quickload(name, type)
    for name, type in [
        ("front_normal", BuildingSpriteSheetSymmetricalX),
        ("front_gate", BuildingSpriteSheetSymmetricalY),  # FIXME not symmetrical, but unused in the back
        ("front_gate_extender", BuildingSpriteSheetSymmetrical),  # ditto
        ("central", BuildingSpriteSheetSymmetrical),
        ("central_windowed", BuildingSpriteSheetSymmetricalY),
        ("central_windowed_extender", BuildingSpriteSheetSymmetrical),
        ("side_a", BuildingSpriteSheetFull),
        ("side_b", BuildingSpriteSheetFull),
        ("side_c", BuildingSpriteSheetSymmetricalY),
        ("corner", BuildingSpriteSheetFull),
    ]
]


def get_back_index(l, r):
    if l + r == 0:
        # FIXME
        return front_normal.T
    if l == 0:
        return corner.TL
    if r == 0:
        return corner.TR
    return front_normal.T


def get_left_index(t, d):
    a = [corner.L, side_a.L, side_b.L, side_c.L, side_b.TL, side_a.TL, corner.TL]
    if t < d:
        return a[min(t, 3)]
    else:
        return a[-1 - min(d, 3)]


left_wall = grf.Switch(
    ranges={
        t: grf.Switch(
            ranges={d: get_left_index(t, d) for d in range(16)},
            default=side_c.L,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=side_c.L,
    code="var(0x41, shift=12, and=0x0000000f)",
)
right_wall = grf.Switch(
    ranges={
        t: grf.Switch(
            ranges={d: get_left_index(t, d).R for d in range(16)},
            default=side_c.R,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=side_c.R,
    code="var(0x41, shift=12, and=0x0000000f)",
)


def get_central_index(l, r):
    if l + r == 0:
        return central
    if l + r == 1:
        return [left_wall, right_wall][l]
    if l + r == 2:
        return [left_wall, central, right_wall][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return (
        [left_wall]
        + [central] * o
        + [central_windowed.L]
        + [central_windowed_extender] * c
        + [central_windowed.R]
        + [central] * o
        + [right_wall]
    )[l]


def get_front_index(l, r):
    if l + r == 0:
        # FIXME
        return corner.L
    if l + r == 1:
        return [corner.L, corner.R][l]
    if l + r == 2:
        # FIXME
        return [corner.L, front_normal.C, corner.R][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return (
        [corner.L]
        + [front_normal] * o
        + [front_gate.L]
        + [front_gate_extender] * c
        + [front_gate.R]
        + [front_normal] * o
        + [corner.R]
    )[l]


cb41 = fixup_callback(
    grf.Switch(
        ranges={
            (0, 1): front_normal,
            (2, 3): grf.Switch(
                ranges={
                    l: grf.Switch(
                        ranges={r: get_back_index(l, r) for r in range(16)},
                        default=front_normal.T,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=front_normal.T,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
            (4, 5): grf.Switch(
                ranges={
                    l: grf.Switch(
                        ranges={r: get_front_index(l, r) for r in range(16)},
                        default=front_normal,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=front_normal,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
            (6, 7): grf.Switch(
                ranges={
                    l: grf.Switch(
                        ranges={r: get_central_index(l, r) for r in range(16)},
                        default=central,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=central,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
        },
        default=central,
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
