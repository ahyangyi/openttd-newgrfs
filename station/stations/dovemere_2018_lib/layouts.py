import os
import grf
from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    BuildingSpriteSheetRotational,
    BuildingSpriteSheetDiagonal,
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
    pl1_low_white_shed_d as platform,
    pl1_low_white_shed as platform_s,
    pl1_low_white_shed_nt as platform_s_nt,
)
from station.stations.ground import sprites as ground_sprites, gray, gray_third, gray_layout
from station.stations.misc import rail


def get_category(internal_category, back, notes):
    if internal_category in ["F0", "F1"]:
        ret = 0x80 + (internal_category[1] == "1")
        if back:
            ret += 0x8
    elif internal_category in ["A", "B", "C", "D"]:
        ret = 0x90 + 0x10 * (ord(internal_category) - ord("A"))
        if "near" in notes:
            ret += 1 ^ (back * 3)
        elif "far" in notes:
            ret += 2 ^ (back * 3)
        elif "both" in notes:
            ret += 3
    elif internal_category == "N":
        ret = 0xF0
    elif internal_category == "H":
        ret = 0xD0
    elif internal_category == "T":
        ret = 0xF1
    elif internal_category == "X":
        ret = 0xF2
    else:
        raise KeyError(f"Unsupported internal category {internal_category}")
    return b"\xe8\x8a\x9c" + ret.to_bytes(1, "little")


def quickload(name, type, traversable, platform, category):
    v = LazyVoxel(
        os.path.basename(name),
        prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(name)),
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    shed_height = 14
    sprite = type.create_variants(v.spritesheet(zdiff=shed_height * 2 if platform else 0))
    sprites.extend(sprite.all_variants)

    if traversable:
        ground = ADefaultGroundSprite(1012)
    else:
        ground = AGroundSprite(gray)
    if platform:
        parent = AParentSprite(sprite, (16, 16, 48 - shed_height), (0, 0, shed_height))
    else:
        parent = AParentSprite(sprite, (16, 16, 48), (0, 0, 0))
    plat = AParentSprite(platform_sprites[4], (16, 6, 6), (0, 10, 0))
    third = AParentSprite(gray_third, (16, 16, 1), (0, 0, 0))

    if platform:
        if type.is_symmetrical_y():
            candidates = [
                ALayout(ground, [parent], traversable),
                ALayout(ground, [plat, parent], traversable, notes=["y", "near"]),
                ALayout(ground, [plat, plat.T, parent], traversable, notes=["both"]),
            ]
        else:
            candidates = [
                ALayout(ground, [parent], traversable),
                ALayout(ground, [plat, parent], traversable, notes=["near"]),
                ALayout(ground, [plat.T, parent], traversable, notes=["far"]),
                ALayout(ground, [plat, plat.T, parent], traversable, notes=["both"]),
            ]
    else:
        if traversable:
            candidates = [ALayout(ground, [third, third.T, parent], traversable)]
        else:
            candidates = [ALayout(ground, [parent], traversable)]

    ret = []
    for l in candidates:
        if "y" in l.notes:
            cur_type = type.break_y_symmetry()
        else:
            cur_type = type
        l = cur_type.get_all_variants(l)
        for i, layout in enumerate(l):
            layout.category = get_category(category, i >= len(l) // 2, layout.notes)
        layouts.extend(l)
        l = cur_type.create_variants(l)
        entries.extend(cur_type.get_all_entries(l))
        ret.append(l)

    if len(ret) == 1:
        return ret[0]
    return ret


sprites = platform_sprites + ground_sprites
layouts = []
entries = []
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
        ("corner", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_gate", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_2", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_gate_2", BuildingSpriteSheetFull, False, False, "F1"),
        ("front_normal", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("front_gate", BuildingSpriteSheetFull, False, False, "F0"),
        ("front_gate_extender", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("central", BuildingSpriteSheetSymmetrical, True, False, "N"),
        ("central_windowed", BuildingSpriteSheetSymmetricalY, True, False, "N"),
        ("central_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "N"),
        ("side_a", BuildingSpriteSheetFull, True, True, "A"),
        ("side_a_windowed", BuildingSpriteSheetFull, True, True, "A"),
        ("side_a2", BuildingSpriteSheetSymmetricalY, True, True, "A"),
        ("side_a2_windowed", BuildingSpriteSheetSymmetricalY, True, True, "A"),
        ("side_a3", BuildingSpriteSheetFull, True, True, "A"),
        ("side_a3_windowed", BuildingSpriteSheetFull, True, True, "A"),
        ("side_b", BuildingSpriteSheetFull, True, True, "B"),
        ("side_b2", BuildingSpriteSheetSymmetricalY, True, True, "B"),
        ("side_c", BuildingSpriteSheetSymmetricalY, True, True, "C"),
        ("side_d", BuildingSpriteSheetSymmetricalY, True, True, "D"),
        ("h_end", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_end_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_end_gate_1", BuildingSpriteSheetFull, True, False, "H"),
        ("h_normal", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_windowed", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("v_end", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("v_end_gate", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("v_central", BuildingSpriteSheetSymmetrical, True, True, "N"),
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
        ("junction/front_corner", BuildingSpriteSheetDiagonal, False, False, "X"),
        ("junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, False, False, "X"),
        ("junction/double_corner_2", BuildingSpriteSheetDiagonal, False, False, "X"),
        ("junction/bicorner", BuildingSpriteSheetDiagonal, False, False, "X"),
    ]
]
