import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    BuildingSpriteSheetRotational,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
    LayoutSprite,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from .platforms import sprites as platform_sprites, pl1_low_white_d as platform, pl1_low_white as platform_s


def quickload(name, type, traversable, platform, category):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.create_variants(v.spritesheet())
    sprites.extend(sprite.all_variants)

    ground = ADefaultGroundSprite(1012 if traversable else 1420)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    plat = AParentSprite(platform_sprites[0], (16, 6, 6), (0, 10, 0))

    if platform:
        if type.is_symmetrical_y():
            candidates = [
                ALayout(ground, [plat, parent], traversable),
                ALayout(ground, [plat, plat.T, parent], traversable),
            ]
        else:
            candidates = [
                ALayout(ground, [plat, parent], traversable),
                ALayout(ground, [plat.T, parent], traversable),
                ALayout(ground, [plat, plat.T, parent], traversable),
            ]
    else:
        candidates = [ALayout(ground, [parent], traversable)]

    ret = []
    for l in candidates:
        l = type.get_all_variants(l)
        for layout in l[: len(l) // 2]:
            layout.category = category
        for layout in l[len(l) // 2 :]:
            layout.category = "B" if category == "F" else category
        layouts.extend(l)
        ret.append(type.create_variants(l))

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = platform_sprites.copy()
layouts = []
(
    corner,
    corner_gate,
    corner_2,
    front_normal,
    front_gate,
    front_gate_extender,
    central,
    central_windowed,
    central_windowed_extender,
    (side_a_n, side_a_f, side_a),
    (side_a_windowed_n, side_a_windowed_f, side_a_windowed),
    (side_a2_n, side_a2),
    (side_a2_windowed_n, side_a2_windowed),
    (side_a3_n, side_a3_f, side_a3),
    (side_a3_windowed_n, side_a3_windowed_f, side_a3_windowed),
    (side_b_n, side_b_f, side_b),
    (side_b2_n, side_b2),
    (side_c_n, side_c),
    (side_d_n, side_d),
    h_end,
    h_normal,
    h_gate,
    h_gate_extender,
    h_windowed,
    h_windowed_extender,
    v_end,
    (v_central_n, v_central),
    tiny,
    turn,
    junction3,
    junction4,
    double_corner,
    funnel,
    inner_corner,
    double_inner_corner,
    v_funnel,
    front_corner,
    front_gate_extender_corner,
    double_corner_2,
    bicorner,
) = [
    quickload(name, type, traversable, platform, category)
    for name, type, traversable, platform, category in [
        ("corner", BuildingSpriteSheetFull, False, False, "F"),
        ("corner_gate", BuildingSpriteSheetFull, False, False, "F"),
        ("corner_2", BuildingSpriteSheetFull, False, False, "F"),
        ("front_normal", BuildingSpriteSheetSymmetricalX, False, False, "F"),
        ("front_gate", BuildingSpriteSheetFull, False, False, "F"),
        ("front_gate_extender", BuildingSpriteSheetSymmetricalX, False, False, "F"),
        ("central", BuildingSpriteSheetSymmetrical, True, False, "C"),
        ("central_windowed", BuildingSpriteSheetSymmetricalY, True, False, "C"),
        ("central_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "C"),
        ("side_a", BuildingSpriteSheetFull, True, True, "I"),
        ("side_a_windowed", BuildingSpriteSheetFull, True, True, "I"),
        ("side_a2", BuildingSpriteSheetSymmetricalY, True, True, "I"),
        ("side_a2_windowed", BuildingSpriteSheetSymmetricalY, True, True, "I"),
        ("side_a3", BuildingSpriteSheetFull, True, True, "I"),
        ("side_a3_windowed", BuildingSpriteSheetFull, True, True, "I"),
        ("side_b", BuildingSpriteSheetFull, True, True, "J"),
        ("side_b2", BuildingSpriteSheetSymmetricalY, True, True, "J"),
        ("side_c", BuildingSpriteSheetSymmetricalY, True, True, "K"),
        ("side_d", BuildingSpriteSheetSymmetricalY, True, True, "L"),
        ("h_end", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_normal", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_windowed", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("v_end", BuildingSpriteSheetSymmetricalX, False, False, "F"),
        ("v_central", BuildingSpriteSheetSymmetrical, True, True, "C"),
        ("tiny", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("irregular/turn", BuildingSpriteSheetFull, True, False, "T"),
        ("irregular/junction3", BuildingSpriteSheetSymmetricalX, True, False, "T"),
        ("irregular/junction4", BuildingSpriteSheetSymmetrical, True, False, "T"),
        ("irregular/double_corner", BuildingSpriteSheetRotational, True, False, "T"),
        ("irregular/funnel", BuildingSpriteSheetFull, True, False, "T"),
        ("irregular/inner_corner", BuildingSpriteSheetFull, True, False, "T"),
        ("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, True, False, "T"),
        ("irregular/v_funnel", BuildingSpriteSheetFull, True, False, "T"),
        ("junction/front_corner", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/front_gate_extender_corner", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/double_corner_2", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/bicorner", BuildingSpriteSheetFull, False, False, "X"),
    ]
]

normal_demo = Demo(
    "Normal 5×7 station layout",
    [
        [corner.T, front_gate.T, front_gate_extender.T, front_gate.TR, corner.TR],
        [side_a_n.T, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.TR],
        [side_b_f.T, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.TR],
        [side_c, central_windowed, central_windowed_extender, central_windowed.R, side_c.R],
        [side_b_f, central_windowed, central_windowed_extender, central_windowed.R, side_b_f.R],
        [side_a_n, central_windowed, central_windowed_extender, central_windowed.R, side_a_n.R],
        [corner, front_gate, front_gate_extender, front_gate.R, corner.R],
    ],
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
sprites.extend(demo_sprites)
demo_layout1 = ALayout(ADefaultGroundSprite(1012), [AParentSprite(demo_sprites[0], (16, 16, 48), (0, 0, 0))], False)
demo_layout2 = ALayout(ADefaultGroundSprite(1011), [AParentSprite(demo_sprites[1], (16, 16, 48), (0, 0, 0))], False)
layouts.append(demo_layout1)
layouts.append(demo_layout2)


def get_back_index(l, r):
    return get_front_index(l, r).T


def get_left_index(t, d):
    if t + d == 2:
        return [corner, side_a2, corner.T][t]
    if t + d == 4:
        return [corner, side_a, side_b2, side_a.T, corner.T][t]
    a = [corner, side_a, side_b, side_c, side_b.T, side_a.T, corner.T]
    if t < d:
        return a[min(t, 3)]
    else:
        return a[-1 - min(d, 3)]


def horizontal_layout(l, r, onetile, lwall, general, window, window_extender):
    if l + r == 0:
        return onetile
    if l + r == 1:
        return [lwall, lwall.R][l]
    if l + r == 2:
        return [lwall, general, lwall.R][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([lwall] + [general] * o + [window] + [window_extender] * c + [window.R] + [general] * o + [lwall.R])[l]


left_wall = Switch(
    ranges={
        t: Switch(
            ranges={d: get_left_index(t, d) for d in range(16)},
            default=side_c,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=side_c,
    code="var(0x41, shift=12, and=0x0000000f)",
)


def get_central_index(l, r):
    return horizontal_layout(l, r, v_central, left_wall, central, central_windowed, central_windowed_extender)


def get_front_index(l, r):
    return horizontal_layout(l, r, v_end, corner, front_normal, front_gate, front_gate_extender)


def get_single_index(l, r):
    return horizontal_layout(l, r, tiny, h_end, h_normal, h_gate, h_gate_extender)


cb14 = Switch(
    ranges={
        (0, 1): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_single_index(l, r) for r in range(16)},
                    default=h_normal,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=h_normal,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (2, 3): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_back_index(l, r) for r in range(16)},
                    default=front_normal.T,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=front_normal.T,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (4, 5): Switch(
            ranges={
                l: Switch(
                    ranges={r: get_front_index(l, r) for r in range(16)},
                    default=front_normal,
                    code="var(0x41, shift=0, and=0x0000000f)",
                )
                for l in range(16)
            },
            default=front_normal,
            code="var(0x41, shift=4, and=0x0000000f)",
        ),
        (6, 7): Switch(
            ranges={
                l: Switch(
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
).to_index(layouts)

the_station = AStation(
    id=0x00,
    translation_name="FLEXIBLE_UNTRAVERSABLE",
    sprites=sprites,
    layouts=[layout.to_grf(sprites) for layout in layouts],
    class_label=b"\xe8\x8a\x9cA",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
    callbacks={
        "select_tile_layout": grf.PurchaseCallback(
            purchase=Switch(
                ranges={
                    (2, 15): Switch(
                        ranges={0: 2},
                        default=Switch(ranges={0: 4}, default=6, code="(extra_callback_info1 >> 12) & 0xf"),
                        code="(extra_callback_info1 >> 8) & 0xf",
                    )
                },
                default=0,
                code="(extra_callback_info1 >> 20) & 0xf",
            )
        ),
        "select_sprite_layout": grf.DualCallback(default=cb14, purchase=layouts.index(demo_layout1)),
    },
)

the_stations = AMetaStation(
    [the_station]
    + [
        AStation(
            id=0x10 + i,
            translation_name="DEFAULT" if layouts[0].traversable else "UNTRAVERSABLE",
            sprites=sprites,  # FIXME
            layouts=[layouts[0].to_grf(sprites), layouts[1].to_grf(sprites)],
            class_label=b"\xe8\x8a\x9c" + layouts[0].category.encode(),
            cargo_threshold=40,
            non_traversable_tiles=0b00 if layouts[0].traversable else 0b11,
            callbacks={"select_tile_layout": 0},
        )
        for i, layouts in enumerate(zip(layouts[:-2:2], layouts[1:-2:2]))
    ],
    b"\xe8\x8a\x9cA",
    ["F", "B", "C", "I", "J", "K", "H", "T", "X"],
    layouts,
    [
        normal_demo,
        Demo(
            "Normal 7×8 station layout",
            [
                [
                    corner.T,
                    front_normal.T,
                    front_gate.T,
                    front_gate_extender.T,
                    front_gate.TR,
                    front_normal.T,
                    corner.TR,
                ],
                [
                    side_a_n.T,
                    central,
                    central_windowed,
                    central_windowed_extender,
                    central_windowed.R,
                    central,
                    side_a_n.TR,
                ],
                [
                    side_b_f.T,
                    central,
                    central_windowed,
                    central_windowed_extender,
                    central_windowed.R,
                    central,
                    side_b_f.TR,
                ],
                [side_c, central, central_windowed, central_windowed_extender, central_windowed.R, central, side_c.R],
                [
                    side_b_f,
                    central,
                    central_windowed,
                    central_windowed_extender,
                    central_windowed.R,
                    central,
                    side_b_f.R,
                ],
                [
                    side_a_n,
                    central,
                    central_windowed,
                    central_windowed_extender,
                    central_windowed.R,
                    central,
                    side_a_n.R,
                ],
                [corner, front_normal, front_gate, front_gate_extender, front_gate.R, front_normal, corner.R],
            ],
        ),
        Demo(
            "Fully traversable automatic stations",
            [
                [
                    tiny,
                    platform,
                    h_end,
                    h_end.R,
                    platform,
                    h_end,
                    h_normal,
                    h_end.R,
                    platform,
                    h_end,
                    h_gate,
                    h_gate.R,
                    h_end.R,
                ],
                [platform] * 13,
                [
                    v_end.T,
                    platform,
                    corner_gate.T,
                    corner_gate.TR,
                    platform,
                    corner_gate.T,
                    front_gate_extender.T,
                    corner_gate.TR,
                    platform,
                    corner_2.T,
                    front_gate.T,
                    front_gate.TR,
                    corner_2.TR,
                ],
                [
                    v_end,
                    platform,
                    corner_gate,
                    corner_gate.R,
                    platform,
                    corner_gate,
                    front_gate_extender,
                    corner_gate.R,
                    platform,
                    corner_2,
                    front_gate,
                    front_gate.R,
                    corner_2.R,
                ],
                [platform] * 13,
                [
                    v_end.T,
                    platform,
                    corner_gate.T,
                    corner_gate.TR,
                    platform,
                    corner_gate.T,
                    front_gate_extender.T,
                    corner_gate.TR,
                    platform,
                    corner.T,
                    front_gate.T,
                    front_gate.TR,
                    corner.TR,
                ],
                [
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
                ],
                [
                    v_end,
                    platform,
                    corner_gate,
                    corner_gate.R,
                    platform,
                    corner_gate,
                    front_gate_extender,
                    corner_gate.R,
                    platform,
                    corner,
                    front_gate,
                    front_gate.R,
                    corner.R,
                ],
                [platform] * 13,
                [
                    v_end.T,
                    platform,
                    corner_gate.T,
                    corner_gate.TR,
                    platform,
                    corner_gate.T,
                    front_gate_extender.T,
                    corner_gate.TR,
                    platform,
                    corner.T,
                    front_gate.T,
                    front_gate.TR,
                    corner.TR,
                ],
                [
                    v_central,
                    platform,
                    side_a3_windowed.T,
                    side_a3_windowed.TR,
                    platform,
                    side_a3_windowed.T,
                    central_windowed_extender,
                    side_a3_windowed.TR,
                    platform,
                    side_a3.T,
                    central_windowed,
                    central_windowed.R,
                    side_a3.TR,
                ],
                [
                    v_central,
                    platform,
                    side_a3_windowed,
                    side_a3_windowed.R,
                    platform,
                    side_a3_windowed,
                    central_windowed_extender,
                    side_a3_windowed.R,
                    platform,
                    side_a3,
                    central_windowed,
                    central_windowed.R,
                    side_a3.R,
                ],
                [
                    v_end,
                    platform,
                    corner_gate,
                    corner_gate.R,
                    platform,
                    corner_gate,
                    front_gate_extender,
                    corner_gate.R,
                    platform,
                    corner,
                    front_gate,
                    front_gate.R,
                    corner.R,
                ],
                [platform] * 13,
                [
                    v_end.T,
                    platform,
                    corner_gate.T,
                    corner_gate.TR,
                    platform,
                    corner_gate.T,
                    front_gate_extender.T,
                    corner_gate.TR,
                    platform,
                    corner.T,
                    front_gate.T,
                    front_gate.TR,
                    corner.TR,
                ],
                [
                    v_central,
                    platform,
                    side_a3_windowed.T,
                    side_a3_windowed.TR,
                    platform,
                    side_a3_windowed.T,
                    central_windowed_extender,
                    side_a3_windowed.TR,
                    platform,
                    side_a.T,
                    central_windowed,
                    central_windowed.R,
                    side_a.TR,
                ],
                [
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
                ],
                [
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
                ],
                [
                    v_end,
                    platform,
                    corner_gate,
                    corner_gate.R,
                    platform,
                    corner_gate,
                    front_gate_extender,
                    corner_gate.R,
                    platform,
                    corner,
                    front_gate,
                    front_gate.R,
                    corner.R,
                ],
            ],
        ),
        Demo(
            "Irregular 7×7 station layout",
            [
                [h_end, junction3.T, h_windowed, h_windowed_extender, h_windowed.R, junction3.T, h_end.R],
                [platform, v_central, platform, platform, platform, v_central, platform],
                [platform, v_central, platform, platform, platform, v_central, platform],
                [platform, v_central, platform, platform, platform, v_central, platform],
                [platform, v_central, platform, platform, platform, v_central, platform],
                [platform, v_central, platform, platform, platform, v_central, platform],
                [h_end, junction3, h_gate, h_gate_extender, h_gate.R, junction3, h_end.R],
            ],
        ),
        Demo(
            "Irregular 7×7 station layout",
            [
                [None, h_end, turn.TR, None, turn.T, h_end.R, None],
                [platform, platform, v_central, platform, v_central, platform, platform],
                [platform, platform, v_central, platform, v_central, platform, platform],
                [h_end, h_windowed, junction4, h_windowed_extender, junction4, h_windowed.R, h_end.R],
                [platform, platform, v_central, platform, v_central, platform, platform],
                [platform, platform, v_central, platform, v_central, platform, platform],
                [None, h_end, turn.R, None, turn, h_end.R, None],
            ],
        ),
        Demo(
            "Irregular 7×7 station layout",
            [
                [corner.T, front_gate.T, front_gate.TR, funnel.TR, h_normal, h_normal, h_end.R],
                [side_a2, central_windowed, central_windowed.R, side_a3.TR, platform, platform, platform],
                [corner, inner_corner, central, side_a3.R, platform, platform, platform],
                [None, corner, front_normal, double_corner.R, front_normal.T, corner.TR, None],
                [platform, platform, platform, side_a3.T, central, inner_corner.TR, corner.TR],
                [platform, platform, platform, side_a3, central_windowed, central_windowed.R, side_a2.R],
                [h_end, h_normal, h_normal, funnel, front_gate, front_gate.R, corner.R],
            ],
        ),
        Demo(
            "Irregular 7×7 station layout",
            [
                [v_end.M, v_central.M, v_central.M, v_central.M, v_central.M, v_funnel.R.M, bicorner.TR],
                [platform.M, platform.M, platform.M, platform.M, corner.R.M, double_corner_2, v_funnel.R],
                [platform.M, platform.M, platform.M, corner.R.M, double_corner_2, corner.R, v_central],
                [platform.M, platform.M, corner.R.M, double_corner_2, corner.R, platform, v_central],
                [platform.M, corner.R.M, double_corner_2, corner.R, platform, platform, v_central],
                [corner_gate.R.M, double_corner_2, corner.R, platform, platform, platform, v_central],
                [front_gate_extender_corner, corner_gate.R, platform, platform, platform, platform, v_end],
            ],
        ),
        Demo(
            "Irregular 7×7 station layout",
            [
                [h_end, junction3.T, h_normal, turn.TR, None, None, None],
                [platform, v_central, platform, v_central, platform, platform, platform],
                [platform, v_central, platform, v_central, platform, platform, platform],
                [platform, v_central, platform, v_central, corner.T, front_normal.T, corner.T.R],
                [platform, v_end, platform, turn, double_inner_corner, central_windowed, side_a2_windowed.R],
                [None, None, None, None, v_funnel, front_normal, corner.R],
                [None, None, None, None, v_end, None, None],
            ],
        ),
    ],
)
