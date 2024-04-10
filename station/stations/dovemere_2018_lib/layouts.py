import os
from station.lib import (
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    BuildingSpriteSheetRotational,
    BuildingSpriteSheetDiagonal,
    ADefaultGroundSprite,
    AGroundSprite,
    AParentSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platforms import (
    sprites as platform_sprites,
    pl1_low_white_d as platform,
    pl1_low_white as platform_s,
    pl1_low_white_nt as platform_s_nt,
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


platform_height = 6
base_height = 16
plat = AParentSprite(platform_sprites[0], (16, 6, platform_height), (0, 10, 0))
plat_nt = AParentSprite(platform_sprites[4], (16, 6, platform_height), (0, 10, 0))
third = AParentSprite(gray_third, (16, 16, 1), (0, 0, 0))


class LoadType:
    def __init__(self, name, symmetry, internal_category):
        self.name = name
        self.symmetry = symmetry
        self.internal_category = internal_category

    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet())
        return [AParentSprite(sprite, (16, 16, 48), (0, 0, 0))]

    def make_platform_variants(self, ground, parents):
        return [ALayout(ground, parents, True)]

    def load(self):
        v = LazyVoxel(
            os.path.basename(self.name),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.name)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.name}.vox": path,
            load_from="station/files/gorender.json",
            subset=self.symmetry.render_indices(),
        )
        ground, fake_ground_sprites = self.get_ground_sprites()
        sprites = self.get_sprites(v)

        candidates = self.make_platform_variants(ground, fake_ground_sprites + sprites)
        ret = []
        for l in candidates:
            if "y" in l.notes:
                cur_sym = self.symmetry.break_y_symmetry()
            else:
                cur_sym = self.symmetry
            l = cur_sym.get_all_variants(l)
            for i, layout in enumerate(l):
                layout.category = get_category(self.internal_category, i >= len(l) // 2, layout.notes)
            layouts.extend(l)
            l = cur_sym.create_variants(l)
            entries.extend(cur_sym.get_all_entries(l))
            ret.append(l)

        if len(ret) == 1:
            return ret[0]
        return ret


class Traversable(LoadType):
    def __init__(self, name, symmetry, internal_category):
        super().__init__(name, symmetry, internal_category)

    def get_ground_sprites(self):
        return ADefaultGroundSprite(1012), []


class TraversablePlatform(Traversable):
    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet(zdiff=platform_height * 2))
        return [AParentSprite(sprite, (16, 16, 48 - platform_height), (0, 0, platform_height))]

    def make_platform_variants(self, ground, parents):
        if self.symmetry.is_symmetrical_y():
            return [
                ALayout(ground, parents, True),
                ALayout(ground, parents + [plat], True, notes=["y", "near"]),
                ALayout(ground, parents + [plat, plat.T], True, notes=["both"]),
            ]
        return [
            ALayout(ground, parents, True),
            ALayout(ground, parents + [plat], True, notes=["near"]),
            ALayout(ground, parents + [plat.T], True, notes=["far"]),
            ALayout(ground, parents + [plat, plat.T], True, notes=["both"]),
        ]


class TraversableCorridor(Traversable):
    def get_ground_sprites(self):
        return ADefaultGroundSprite(1012), [third, third.T]


class Side(LoadType):
    def get_ground_sprites(self):
        return AGroundSprite(gray), []


class SideFull(Side):
    def get_sprites(self, voxel):
        f1v = voxel.mask_clip("station/voxels/dovemere_2018/masks/ground_level.vox", "f1")
        f2v = voxel.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f1 = self.symmetry.create_variants(f1v.spritesheet())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(f1, (16, 16, 48), (0, 0, 0)), AParentSprite(f2, (16, 16, 32), (0, 0, base_height))]


class SidePlatform(Side):
    def get_sprites(self, voxel):
        f1v = voxel.mask_clip("station/voxels/dovemere_2018/masks/ground_level.vox", "f1")
        f2v = voxel.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f1 = self.symmetry.create_variants(f1v.spritesheet(xdiff=6))
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(f1, (16, 10, 48), (0, 6, 0)), AParentSprite(f2, (16, 16, 32), (0, 0, base_height))]

    def make_platform_variants(self, ground, parents):
        return [ALayout(ground, parents + [plat_nt.T], True)]


class SideThird(Traversable):
    def get_sprites(self, voxel):
        f1v = voxel.mask_clip("station/voxels/dovemere_2018/masks/ground_level.vox", "f1")
        f2v = voxel.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f1 = self.symmetry.create_variants(f1v.spritesheet(xdiff=10))
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(f1, (16, 6, 48), (0, 10, 0)), AParentSprite(f2, (16, 16, 32), (0, 0, base_height))]

    def make_platform_variants(self, ground, parents):
        return [ALayout(ground, parents, True), ALayout(ground, parents + [plat.T], True)]


def quickload(name, type, traversable, platform, category):
    worker_class = {
        (True, True): TraversablePlatform,
        (True, False): TraversableCorridor,
        (True, "third"): SideThird,
        (False, True): SidePlatform,
        (False, False): SideFull,
    }[(traversable, platform)]

    worker = worker_class(name, type, category)
    return worker.load()


layouts = []
entries = []
(
    corner,
    corner_platform,
    (corner_third, corner_third_f),
    corner_gate,
    corner_gate_platform,
    (corner_gate_third, corner_gate_third_f),
    corner_2,
    (corner_2_third, corner_2_third_f),
    corner_gate_2,
    (corner_gate_2_third, corner_gate_2_third_f),
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
    h_end_asym,
    h_end_asym_platform,
    h_end_gate,
    h_end_gate_1,
    h_normal,
    h_gate,
    h_gate_1_platform,
    h_gate_extender,
    h_gate_extender_1_platform,
    h_windowed,
    h_windowed_extender,
    v_end,
    v_end_platform,
    (v_end_third, v_end_third_f),
    v_end_gate,
    v_end_gate_platform,
    (v_end_gate_third, v_end_gate_third_f),
    (v_central_x, v_central_n, v_central),
    tiny,
    turn,
    turn_gate,
    tee,
    tee_platform,
    cross,
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
        ("corner_platform", BuildingSpriteSheetFull, False, True, "F1"),
        ("corner_third", BuildingSpriteSheetFull, True, "third", "F1"),
        ("corner_gate", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_gate_platform", BuildingSpriteSheetFull, False, True, "F1"),
        ("corner_gate_third", BuildingSpriteSheetFull, True, "third", "F1"),
        ("corner_2", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_2_third", BuildingSpriteSheetFull, True, "third", "F1"),
        ("corner_gate_2", BuildingSpriteSheetFull, False, False, "F1"),
        ("corner_gate_2_third", BuildingSpriteSheetFull, True, "third", "F1"),
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
        ("h_end_asym", BuildingSpriteSheetFull, False, False, "H"),
        ("h_end_asym_platform", BuildingSpriteSheetFull, False, True, "H"),
        ("h_end_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_end_gate_1", BuildingSpriteSheetFull, True, False, "H"),
        ("h_normal", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_gate_1_platform", BuildingSpriteSheetFull, False, True, "H"),
        ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("h_gate_extender_1_platform", BuildingSpriteSheetFull, False, True, "H"),
        ("h_windowed", BuildingSpriteSheetSymmetricalY, True, False, "H"),
        ("h_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("v_end", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("v_end_platform", BuildingSpriteSheetSymmetricalX, False, True, "F0"),
        ("v_end_third", BuildingSpriteSheetSymmetricalX, True, "third", "F0"),
        ("v_end_gate", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
        ("v_end_gate_platform", BuildingSpriteSheetSymmetricalX, False, True, "F0"),
        ("v_end_gate_third", BuildingSpriteSheetSymmetricalX, True, "third", "F0"),
        ("v_central", BuildingSpriteSheetSymmetrical, True, True, "N"),
        ("tiny", BuildingSpriteSheetSymmetrical, True, False, "H"),
        ("irregular/turn", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/turn_gate", BuildingSpriteSheetFull, False, False, "T"),
        ("irregular/tee", BuildingSpriteSheetSymmetricalX, False, False, "T"),
        ("irregular/tee_platform", BuildingSpriteSheetSymmetricalX, False, True, "T"),
        ("irregular/cross", BuildingSpriteSheetSymmetrical, False, False, "T"),
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
