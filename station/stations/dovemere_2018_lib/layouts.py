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

    if traversable:
        ground = ADefaultGroundSprite(1012)
    else:
        ground = AGroundSprite(gray)
    parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    plat = AParentSprite(platform_sprites[0], (16, 6, 6), (0, 10, 0))
    third = AParentSprite(gray_third, (16, 16, 1), (0, 0, 0))

    if platform:
        if type.is_symmetrical_y():
            candidates = [
                ALayout(ground, [plat, parent], traversable, notes=["y"]),
                ALayout(ground, [plat, plat.T, parent], traversable),
            ]
        else:
            candidates = [
                ALayout(ground, [plat, parent], traversable),
                ALayout(ground, [plat.T, parent], traversable),
                ALayout(ground, [plat, plat.T, parent], traversable),
            ]
    else:
        if traversable:
            candidates = [ALayout(ground, [third, third.T, parent], traversable)]
        else:
            candidates = [ALayout(ground, [parent], traversable)]

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
    corner_gate,
    corner_2,
    corner_gate_2,
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
    h_end_gate,
    h_end_gate_1,
    h_normal,
    h_gate,
    h_gate_extender,
    h_windowed,
    h_windowed_extender,
    v_end,
    v_end_gate,
    (v_central_n, v_central),
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
