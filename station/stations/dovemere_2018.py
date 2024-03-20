import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    Demo,
    fixup_callback,
    simple_layout,
)
from agrf.graphics.voxel import LazyVoxel


def quickload(name, type, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
    )
    ret = type.from_complete_list(v.spritesheet())
    sprites.extend(ret.all())
    for sprite in ret.all_variants():
        layouts.append((sprite, traversable))
    return ret


sprites = []
layouts = []
(
    corner,
    front_normal,
    front_gate,
    front_gate_extender,
    central,
    central_windowed,
    central_windowed_extender,
    side_a,
    side_a2,
    side_b,
    side_b2,
    side_c,
    h_end,
    h_normal,
) = [
    quickload(name, type, traversable)
    for name, type, traversable in [
        ("corner", BuildingSpriteSheetFull, False),
        ("front_normal", BuildingSpriteSheetSymmetricalX, False),
        ("front_gate", BuildingSpriteSheetFull, False),
        ("front_gate_extender", BuildingSpriteSheetSymmetricalX, False),
        ("central", BuildingSpriteSheetSymmetrical, True),
        ("central_windowed", BuildingSpriteSheetSymmetricalY, True),
        ("central_windowed_extender", BuildingSpriteSheetSymmetrical, True),
        ("side_a", BuildingSpriteSheetFull, True),
        ("side_a2", BuildingSpriteSheetSymmetricalY, True),
        ("side_b", BuildingSpriteSheetFull, True),
        ("side_b2", BuildingSpriteSheetSymmetricalY, True),
        ("side_c", BuildingSpriteSheetSymmetricalY, True),
        ("h_end", BuildingSpriteSheetSymmetricalY, True),
        ("h_normal", BuildingSpriteSheetSymmetrical, True),
    ]
]


def get_back_index(l, r):
    return get_front_index(l, r).T


def get_left_index(t, d):
    if t + d == 2:
        return [corner.L, side_a2.L, corner.TL][t]
    if t + d == 4:
        return [corner.L, side_a.L, side_b2.L, side_a.TL, corner.TL][t]
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


def get_single_index(l, r):
    if l + r == 0:
        # FIXME
        return h_normal
    if l + r == 1:
        # FIXME
        return [h_end.L, h_end.R][l]
    if l + r == 2:
        # FIXME
        return [h_end.L, h_normal, h_end.R][l]

    if l == 0:
        return h_end.L
    if r == 0:
        return h_end.R
    return h_normal


cb41 = fixup_callback(
    grf.Switch(
        ranges={
            (0, 1): grf.Switch(
                ranges={
                    l: grf.Switch(
                        ranges={r: get_single_index(l, r) for r in range(16)},
                        default=h_normal,
                        code="var(0x41, shift=0, and=0x0000000f)",
                    )
                    for l in range(16)
                },
                default=h_normal,
                code="var(0x41, shift=4, and=0x0000000f)",
            ),
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
    ),
    sprites,
)

the_station = AStation(
    id=0x00,
    translation_name="DOVEMERE_2018",
    sprites=sprites,
    layouts=[
        simple_layout(1012 - i % 2 if traversable else 1420, sprites.index(s.sprite))
        for i, (s, traversable) in enumerate(layouts)
    ],
    class_label=b"DM18",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
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

the_stations = AMetaStation(
    [the_station]
    + [
        AStation(
            id=1 + i,
            translation_name="DOVEMERE_2018",  # FIXME
            sprites=[s.sprite for s, _ in layouts],
            layouts=[
                simple_layout(1012 - i % 2 if traversable else 1420, i) for i, (s, traversable) in enumerate(layouts)
            ],
            class_label=b"DM18",
            cargo_threshold=40,
            non_traversable_tiles=0b00 if layouts[0][1] else 0b11,
            callbacks={
                "select_tile_layout": 0,
            },
        )
        for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"DM18",
    [layouts[0][0] for i, layouts in enumerate(zip(layouts[::2], layouts[1::2]))],
    [
        Demo(
            "Normal 4×6 station layout",
            [
                [corner.TL, front_gate.TL, front_gate.TR, corner.TR],
                [side_a.TL, central_windowed.L, central_windowed.R, side_a.TR],
                [side_b.TL, central_windowed.L, central_windowed.R, side_b.TR],
                [side_b.L, central_windowed.L, central_windowed.R, side_b.R],
                [side_a.L, central_windowed.L, central_windowed.R, side_a.R],
                [corner.L, front_gate.L, front_gate.R, corner.R],
            ],
        ),
        Demo(
            "Normal 5×7 station layout",
            [
                [corner.TL, front_gate.TL, front_gate_extender.T, front_gate.TR, corner.TR],
                [side_a.TL, central_windowed.L, central_windowed_extender, central_windowed.R, side_a.TR],
                [side_b.TL, central_windowed.L, central_windowed_extender, central_windowed.R, side_b.TR],
                [side_c.L, central_windowed.L, central_windowed_extender, central_windowed.R, side_c.R],
                [side_b.L, central_windowed.L, central_windowed_extender, central_windowed.R, side_b.R],
                [side_a.L, central_windowed.L, central_windowed_extender, central_windowed.R, side_a.R],
                [corner.L, front_gate.L, front_gate_extender, front_gate.R, corner.R],
            ],
        ),
        Demo(
            "A 3×10 station layout, demonstrating horizontal extensibility",
            [
                [
                    corner.TL,
                    front_normal.T,
                    front_normal.T,
                    front_gate.TL,
                    front_gate_extender.T,
                    front_gate_extender.T,
                    front_gate.TR,
                    front_normal.T,
                    front_normal.T,
                    corner.TR,
                ],
                [
                    side_a2.L,
                    central,
                    central_windowed.L,
                    central_windowed_extender,
                    central_windowed.R,
                    central_windowed.L,
                    central_windowed_extender,
                    central_windowed.R,
                    central,
                    side_a2.R,
                ],
                [
                    corner.L,
                    front_normal,
                    front_normal,
                    front_gate.L,
                    front_gate_extender,
                    front_gate_extender,
                    front_gate.R,
                    front_normal,
                    front_normal,
                    corner.R,
                ],
            ],
        ),
        Demo(
            "A 1×6 station layout",
            [
                [
                    h_end.L,
                    h_normal,
                    front_gate.L,
                    front_gate.R,
                    h_normal,
                    h_end.R,
                ],
            ],
        ),
        Demo(
            "A 6×2 station layout",
            [
                [corner.TL, corner.TR],
                [side_a.TL, side_a.TR],
                [side_b.TL, side_b.TR],
                [side_b.L, side_b.R],
                [side_a.L, side_a.R],
                [corner.L, corner.R],
            ],
        ),
        Demo(
            "A 5×2 station layout",
            [
                [corner.TL, corner.TR],
                [side_a.TL, side_a.TR],
                [side_b2.L, side_b2.R],
                [side_a.L, side_a.R],
                [corner.L, corner.R],
            ],
        ),
    ],
)
