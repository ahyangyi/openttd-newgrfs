import grf
from station.lib import AStation, AMetaStation, Demo, LayoutSprite
from agrf.magic import Switch
from .dovemere_2018_lib.layouts import *
from .dovemere_2018_lib.demos import *


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
        big_demo,
        big_half_demo,
        full_auto_demo,
        semi_auto_demo,
        special_demo_g,
        special_demo_p,
        special_demo_cn,
        special_demo_sa,
        special_demo_cp,
        special_demo_aq,
    ],
)
