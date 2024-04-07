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
    AGroundSprite,
    AParentSprite,
    ALayout,
    LayoutSprite,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from station.stations.platforms import (
    sprites as platform_sprites,
    pl1_low_white_d as platform,
    pl1_low_white as platform_s,
    pl1_low_white_nt as platform_s_nt,
)
from station.stations.ground import sprites as ground_sprites, gray, gray_third, gray_layout
from station.stations.misc import rail


def quickload(name, type, traversable, platform, category):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    if not traversable and platform:
        f1 = v.mask_clip("station/voxels/dovemere_2018/masks/ground_level.vox", "f1")
        f2 = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f1 = type.create_variants(f1.spritesheet(xdiff=6))
        f2 = type.create_variants(f2.spritesheet(zdiff=32))
        sprites.extend(f1.all_variants)
        sprites.extend(f2.all_variants)
    else:
        sprite = type.create_variants(v.spritesheet())
        sprites.extend(sprite.all_variants)

    if traversable:
        ground = ADefaultGroundSprite(1012)
    else:
        ground = AGroundSprite(gray)
    if not traversable and platform:
        parents = [AParentSprite(f1, (16, 10, 48), (0, 6, 0)), AParentSprite(f2, (16, 16, 32), (0, 0, 16))]
        plat = AParentSprite(platform_sprites[4], (16, 6, 6), (0, 10, 0))
    else:
        parents = [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))]
        plat = AParentSprite(platform_sprites[0], (16, 6, 6), (0, 10, 0))
    third = AParentSprite(gray_third, (16, 16, 1), (0, 0, 0))

    if traversable:
        if platform:
            if type.is_symmetrical_y():
                candidates = [
                    ALayout(ground, parents, True),
                    ALayout(ground, parents + [plat], True, notes=["y"]),
                    ALayout(ground, parents + [plat, plat.T], True),
                ]
            else:
                candidates = [
                    ALayout(ground, parents, True),
                    ALayout(ground, parents + [plat], True),
                    ALayout(ground, parents + [plat.T], True),
                    ALayout(ground, parents + [plat, plat.T], True),
                ]
        else:
            candidates = [ALayout(ground, parents + [third, third.T], True)]
    else:
        if platform:
            candidates = [ALayout(ground, parents + [plat.T], False)]
        else:
            candidates = [ALayout(ground, parents, False)]

    ret = []
    for l in candidates:
        if "y" in l.notes:
            cur_type = {
                BuildingSpriteSheetSymmetricalY: BuildingSpriteSheetFull,
                BuildingSpriteSheetSymmetrical: BuildingSpriteSheetSymmetricalX,
                BuildingSpriteSheetRotational: BuildingSpriteSheetFull,
            }.get(type, type)
        else:
            cur_type = type
        l = cur_type.get_all_variants(l)
        for layout in l[: len(l) // 2]:
            layout.category = category
        for layout in l[len(l) // 2 :]:
            layout.category = "B" if category == "F" else category
        layouts.extend(l)
        ret.append(cur_type.create_variants(l))

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = platform_sprites + ground_sprites
layouts = []
(
    corner,
    corner_platform,
    corner_gate,
    corner_2,
    corner_gate_2,
    front_normal,
    front_gate,
    front_gate_extender,
    central,
    central_windowed,
    central_windowed_extender,
    (side_a_x, side_a_n, side_a_f, side_a),
    (side_a_windowed_x, side_a_windowed_n, side_a_windowed_f, side_a_windowed),
    (side_a2_x, side_a2_n, side_a2),
    (side_a2_windowed_x, side_a2_windowed_n, side_a2_windowed),
    (side_a3_x, side_a3_n, side_a3_f, side_a3),
    (side_a3_windowed_x, side_a3_windowed_n, side_a3_windowed_f, side_a3_windowed),
    (side_b_x, side_b_n, side_b_f, side_b),
    (side_b2_x, side_b2_n, side_b2),
    (side_c_x, side_c_n, side_c),
    (side_d_x, side_d_n, side_d),
    h_end,
    h_end_gate,
    h_end_gate_1,
    h_normal,
    h_gate,
    h_gate_extender,
    h_windowed,
    h_windowed_extender,
    v_end,
    v_end_gate,
    (v_central_x, v_central_n, v_central),
    tiny,
    turn,
    turn_gate,
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
        ("corner_platform", BuildingSpriteSheetFull, False, True, "F"),
        ("corner_gate", BuildingSpriteSheetFull, False, False, "F"),
        ("corner_2", BuildingSpriteSheetFull, False, False, "F"),
        ("corner_gate_2", BuildingSpriteSheetFull, False, False, "F"),
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
        ("h_end_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_end_gate_1", BuildingSpriteSheetFull, True, False, "H"),
        ("h_normal", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_windowed", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("v_end", BuildingSpriteSheetSymmetricalX, False, False, "F"),
        ("v_end_gate", BuildingSpriteSheetSymmetricalX, False, False, "F"),
        ("v_central", BuildingSpriteSheetSymmetrical, True, True, "C"),
        ("tiny", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("irregular/turn", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/turn_gate", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/junction3", BuildingSpriteSheetSymmetricalX, False, False, "T"),
        ("irregular/junction4", BuildingSpriteSheetSymmetrical, False, False, "T"),
        ("irregular/double_corner", BuildingSpriteSheetRotational, False, False, "T"),
        ("irregular/funnel", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/inner_corner", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, False, False, "T"),
        ("irregular/v_funnel", BuildingSpriteSheetFull, False, False, "T"),
        ("junction/front_corner", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/front_gate_extender_corner", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/double_corner_2", BuildingSpriteSheetFull, False, False, "X"),
        ("junction/bicorner", BuildingSpriteSheetFull, False, False, "X"),
    ]
]
