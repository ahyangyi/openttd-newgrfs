import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    Demo,
    ADefaultGroundSprite,
    AParentSprite,
    ALayout,
)
from pygorender import Config
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from agrf.graphics.imagesprite import ImageSprite
from .platforms import sprites as platform_sprites


def quickload(name, type, traversable, platform):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.from_complete_list(v.spritesheet())
    sprites.extend(sprite.all_variants)

    ground = ADefaultGroundSprite(1012 if traversable else 1420)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    plat = AParentSprite(platform_sprites[0], (16, 6, 6), (0, 10, 0))

    if platform:
        candidates = [
            ALayout(ground, [plat, parent]),
            ALayout(ground, [plat.T, parent]),
            ALayout(ground, [plat, plat.T, parent]),
        ]
    else:
        candidates = [ALayout(ground, [parent])]

    ret = []
    for l in candidates:
        # FIXME
        if type is BuildingSpriteSheetFull:
            l = [l, l.M, l.R, l.R.M, l.T, l.T.M, l.T.R, l.T.R.M]
            layouts.extend(l)
            ret.append(type.from_complete_list(l))
        elif type is BuildingSpriteSheetSymmetricalX:
            l = [l, l.M, l.T, l.T.M]
            layouts.extend(l)
            ret.append(type.from_complete_list(l))
        elif type is BuildingSpriteSheetSymmetricalY:
            l = [l, l.M, l.R, l.R.M]
            layouts.extend(l)
            ret.append(type.from_complete_list(l))
        else:
            l = [l, l.M]
            layouts.extend(l)
            ret.append(type.from_complete_list(l))

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = platform_sprites.copy()
layouts = []
(
    corner,
    front_normal,
    front_gate,
    front_gate_extender,
    central,
    central_windowed,
    central_windowed_extender,
    (side_a_n, side_a_f, side_a),
    (side_a2_n, side_2a_f, side_a2),
    (side_b_n, side_b_f, side_b),
    (side_b2_n, side_b2_f, side_b2),
    (side_c_n, side_c_f, side_c),
    h_end,
    h_normal,
    h_gate,
    h_gate_extender,
    v_end,
    (v_central_n, v_central_f, v_central),
    tiny,
) = [
    quickload(name, type, traversable, platform)
    for name, type, traversable, platform in [
        ("corner", BuildingSpriteSheetFull, False, False),
        ("front_normal", BuildingSpriteSheetSymmetricalX, False, False),
        ("front_gate", BuildingSpriteSheetFull, False, False),
        ("front_gate_extender", BuildingSpriteSheetSymmetricalX, False, False),
        ("central", BuildingSpriteSheetSymmetrical, True, False),
        ("central_windowed", BuildingSpriteSheetSymmetricalY, True, False),
        ("central_windowed_extender", BuildingSpriteSheetSymmetrical, True, False),
        ("side_a", BuildingSpriteSheetFull, True, True),
        ("side_a2", BuildingSpriteSheetSymmetricalY, True, True),
        ("side_b", BuildingSpriteSheetFull, True, True),
        ("side_b2", BuildingSpriteSheetSymmetricalY, True, True),
        ("side_c", BuildingSpriteSheetSymmetricalY, True, True),
        ("h_end", BuildingSpriteSheetSymmetricalY, True, False),
        ("h_normal", BuildingSpriteSheetSymmetrical, True, False),
        ("h_gate", BuildingSpriteSheetSymmetricalY, True, False),
        ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False),
        ("v_end", BuildingSpriteSheetSymmetricalX, False, False),
        ("v_central", BuildingSpriteSheetSymmetrical, True, True),
        ("tiny", BuildingSpriteSheetSymmetrical, True, False),
    ]
]

normal_demo = Demo(
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
)
from PIL import Image

demo_sprites = []
for i, demo in enumerate([normal_demo, normal_demo.M]):
    img, mask = demo.graphics()
    img.thumbnail((256, 256), Image.Resampling.LANCZOS)
    mask.thumbnail((256, 256), Image.Resampling.LANCZOS)
    sprite = grf.AlternativeSprites(
        grf.WithMask(
            ImageSprite(
                img,
                f"dovemere18_thumbnail_{i}",
                xofs=-128,
                yofs=-64,
                zoom=grf.ZOOM_4X,
            ),
            ImageSprite(
                mask,
                f"dovemere18_thumbnail_mask_{i}",
            ),
        ),
    )
    demo_sprites.append(sprite)
sprites.extend(demo_sprites)
demo_layout1 = ALayout(ADefaultGroundSprite(1012), [AParentSprite(demo_sprites[0], (16, 16, 48), (0, 0, 0))])
demo_layout2 = ALayout(ADefaultGroundSprite(1011), [AParentSprite(demo_sprites[1], (16, 16, 48), (0, 0, 0))])
layouts.append(demo_layout1)
layouts.append(demo_layout2)


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


def horizontal_layout(l, r, onetile, lwall, rwall, general, window, window_extender):
    if l + r == 0:
        return onetile
    if l + r == 1:
        return [lwall, rwall][l]
    if l + r == 2:
        return [lwall, general, rwall][l]

    e = l + r - 3
    c = (e + 1) // 3
    if c % 2 != e % 2:
        c += 1
    o = (e - c) // 2
    return ([lwall] + [general] * o + [window.L] + [window_extender] * c + [window.R] + [general] * o + [rwall])[l]


left_wall = Switch(
    ranges={
        t: Switch(
            ranges={d: get_left_index(t, d) for d in range(16)},
            default=side_c.L,
            code="var(0x41, shift=8, and=0x0000000f)",
        )
        for t in range(16)
    },
    default=side_c.L,
    code="var(0x41, shift=12, and=0x0000000f)",
)

right_wall = left_wall.R


def get_central_index(l, r):
    return horizontal_layout(
        l, r, v_central, left_wall, right_wall, central, central_windowed, central_windowed_extender
    )


def get_front_index(l, r):
    return horizontal_layout(l, r, v_end, corner.L, corner.R, front_normal, front_gate, front_gate_extender)


def get_single_index(l, r):
    return horizontal_layout(l, r, tiny, h_end.L, h_end.R, h_normal, h_gate, h_gate_extender)


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
    translation_name="DOVEMERE_2018",
    sprites=sprites,
    layouts=[layout.to_grf(sprites) for layout in layouts],
    class_label=b"DM18",
    cargo_threshold=40,
    non_traversable_tiles=0b00111100,
    callbacks={
        "select_tile_layout": grf.PurchaseCallback(
            purchase=Switch(
                ranges={
                    (2, 15): Switch(
                        ranges={0: 2},
                        default=Switch(
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
            default=cb14,
            purchase=layouts.index(demo_layout1),
        ),
    },
)

the_stations = AMetaStation(
    [the_station]
    + [
        AStation(
            id=1 + i,
            translation_name="DOVEMERE_2018",  # FIXME
            sprites=sprites,  # FIXME
            layouts=[
                layouts[0].to_grf(sprites),
                layouts[1].to_grf(sprites),
            ],
            class_label=b"DM18",
            cargo_threshold=40,
            non_traversable_tiles=0b00,  # FIXME
            callbacks={
                "select_tile_layout": 0,
            },
        )
        for i, layouts in enumerate(zip(layouts[:-2:2], layouts[1:-2:2]))
    ],
    b"DM18",
    layouts,
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
        normal_demo,
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
            "A 1×7 station layout",
            [
                [
                    h_end.L,
                    h_normal,
                    h_gate.L,
                    h_gate_extender,
                    h_gate.R,
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
        Demo(
            "A 3×1 station layout",
            [
                [v_end.T],
                [v_central],
                [v_end],
            ],
        ),
        Demo(
            "A 1×1 station layout",
            [
                [tiny],
            ],
        ),
    ],
)
