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
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platforms import (
    named_sprites as platform_sprites,
    pl1_low_white_shed_d as platform,
    pl1_low_white_shed as platform_s,
    pl1_low_white_side_shed as platform_s_nt,
)
from station.stations.ground import gray, gray_third, gray_layout
from station.stations.misc import rail


def get_category(internal_category, back, notes):
    if internal_category in ["F0", "F1"]:
        ret = 0x80
        if "far" in notes:
            ret += 0x1
        if "third" in notes:
            ret += 0x2
        if internal_category[1] == "1":
            ret += 0x4
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


platform_height = 15
base_height = 16
building_height = 48
overpass_height = building_height - base_height
plat = AParentSprite(platform_sprites.pl1_low_white, (16, 6, platform_height), (0, 10, 0))
plat_nt = AParentSprite(platform_sprites.pl1_low_white_side, (16, 6, platform_height), (0, 10, 0))
plat_shed = AParentSprite(platform_sprites.pl1_low_white_shed_building, (16, 6, platform_height), (0, 10, 0))
plat_shed_nt = AParentSprite(platform_sprites.pl1_low_white_side_shed, (16, 6, platform_height), (0, 10, 0))
third = AParentSprite(gray_third, (16, 16, 1), (0, 0, 0))


class LoadType:
    def __init__(self, name, source, symmetry, internal_category):
        self.name = name
        self.source = source
        self.symmetry = symmetry
        self.internal_category = internal_category

    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet())
        return [AParentSprite(sprite, (16, 16, building_height), (0, 0, 0))]

    def make_platform_variants(self, ground, parents):
        self.register(ALayout(ground, parents, True))

    def load(self):
        if isinstance(self.source, str):
            v = LazyVoxel(
                os.path.basename(self.source),
                prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.source)),
                voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.source}.vox": path,
                load_from="station/files/gorender.json",
                subset=self.symmetry.render_indices(),
            )
        else:
            v = self.source
        self.do_work(v)

    def do_work(self, v):
        ground, fake_ground_sprites = self.get_ground_sprites()
        sprites = self.get_sprites(v)

        self.make_platform_variants(ground, fake_ground_sprites + sprites)

    def register(self, l, suffix=""):
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
        named_tiles[self.name + suffix] = l


class Traversable(LoadType):
    def get_ground_sprites(self):
        return ADefaultGroundSprite(1012), []


class TraversablePlatform(Traversable):
    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(sprite, (16, 16, overpass_height), (0, 0, base_height))]

    def make_platform_variants(self, ground, parents):
        if self.symmetry.is_symmetrical_y():
            self.register(ALayout(ground, parents, True), "_x")
            self.register(ALayout(ground, parents + [plat], True, notes=["y", "near"]), "_n")
            self.register(ALayout(ground, parents + [plat, plat.T], True, notes=["both"]))
        else:
            self.register(ALayout(ground, parents, True), "_x")
            self.register(ALayout(ground, parents + [plat], True, notes=["near"]), "_n")
            self.register(ALayout(ground, parents + [plat.T], True, notes=["near"]), "_f")
            self.register(ALayout(ground, parents + [plat, plat.T], True, notes=["both"]))


class TraversablePlatformSide(Traversable):
    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(sprite, (16, 16, overpass_height), (0, 0, base_height))]

    def make_platform_variants(self, ground, parents):
        if self.symmetry.is_symmetrical_y():
            self.register(ALayout(ground, parents, True), "_x")
            self.register(ALayout(ground, parents + [plat_shed], True, notes=["y", "near"]), "_n")
            self.register(ALayout(ground, parents + [plat_shed, plat_shed.T], True, notes=["both"]))
        else:
            self.register(ALayout(ground, parents, True), "_x")
            self.register(ALayout(ground, parents + [plat_shed], True, notes=["near"]), "_n")
            self.register(ALayout(ground, parents + [plat_shed.T], True, notes=["near"]), "_f")
            self.register(ALayout(ground, parents + [plat_shed, plat_shed.T], True, notes=["both"]))


class TraversableCorridor(Traversable):
    def get_ground_sprites(self):
        return ADefaultGroundSprite(1012), [third, third.T]


class Side(LoadType):
    def get_ground_sprites(self):
        return AGroundSprite(gray), []


class TwoFloorMixin:
    def get_sprites(self, voxel):
        if isinstance(voxel, tuple):
            f1base, f2 = voxel
        else:
            f1base = f2base = voxel
            f2v = f2base.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
            f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        f1v = f1base.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1 = self.symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x))
        return [
            AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, 0)),
            AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height)),
        ]


class SideFull(TwoFloorMixin, Side):
    f1x = 16


class SidePlatform(TwoFloorMixin, Side):
    f1x = 10

    def make_platform_variants(self, ground, parents):
        self.register(ALayout(ground, parents + [plat_shed_nt.T], True, notes=["far"]))


class SideThird(TwoFloorMixin, Traversable):
    f1x = 6

    def make_platform_variants(self, ground, parents):
        self.register(ALayout(ground, parents, True, notes=["third"]))
        self.register(ALayout(ground, parents + [plat_shed.T], True, notes=["third", "far"]), "_f")


class HorizontalSingle(Traversable):
    def load(self):
        v = LazyVoxel(
            os.path.basename(self.source),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.source}.vox": path,
            load_from="station/files/gorender.json",
        )
        self.do_work(v)

    f1x = 6

    def do_work(self, v):
        ground, fake_ground_sprites = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2v.in_place_subset(self.symmetry.render_indices())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1v = v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1_symmetry = self.symmetry.break_y_symmetry()
        f1v.in_place_subset(f1_symmetry.render_indices())
        f1 = f1_symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x))

        f1s = AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, 0))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height))

        self.register(ALayout(ground, [f1s, f1s.T, f2s], True), "")
        self.register(ALayout(ground, [f1s, f2s], True, notes=["third", "y"]), "_third")
        self.register(ALayout(ground, [f1s, f2s, plat_shed.T], True, notes=["third", "y", "far"]), "_third_f")


class HorizontalSingleAsym(Traversable):
    def load(self):
        v = LazyVoxel(
            os.path.basename(self.source),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.source}.vox": path,
            load_from="station/files/gorender.json",
        )
        self.do_work(v)

    f1x = 6

    def do_work(self, v):
        ground, fake_ground_sprites = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2v.in_place_subset(self.symmetry.render_indices())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1v = v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1vb = v.mask_clip_away("station/voxels/dovemere_2018/masks/front.vox", "f1")
        f1vf = v.mask_clip_away("station/voxels/dovemere_2018/masks/back.vox", "f1")
        f1_symmetry = self.symmetry.break_y_symmetry()
        f1vb.in_place_subset(f1_symmetry.render_indices())
        f1vf.in_place_subset(f1_symmetry.render_indices())
        f1f = f1_symmetry.create_variants(f1vf.spritesheet(xdiff=16 - self.f1x))
        f1b = f1_symmetry.create_variants(f1vb.spritesheet())

        f1fs = AParentSprite(f1f, (16, self.f1x, base_height), (0, 16 - self.f1x, 0))
        f1bs = AParentSprite(f1b, (16, self.f1x, base_height), (0, 0, 0))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height))

        self.register(ALayout(ground, [f1fs, f1bs, f2s], True), "")
        self.register(ALayout(ground, [f1fs, f2s], True, notes=["third", "y"]), "_third")
        self.register(ALayout(ground, [f1fs, f2s, plat_shed.T], True, notes=["third", "y", "far"]), "_third_f")


class HorizontalDouble(LoadType):
    def load(self):
        v = LazyVoxel(
            os.path.basename(self.source),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.source}.vox": path,
            load_from="station/files/gorender.json",
        )
        self.do_work(v)

    def do_work(self, v):
        plat_symmetry = self.symmetry.break_y_symmetry()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2v.in_place_subset(plat_symmetry.render_indices())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        corridor = v.discard_layers(("ground level - platform",), "full")
        corridor.in_place_subset(self.symmetry.render_indices())

        plat_f1 = v.discard_layers(("ground level",), "platform")
        plat_f1.in_place_subset(plat_symmetry.render_indices())

        TraversableCorridor(
            self.name, corridor, self.symmetry, self.internal_category  # XXX not a two-floor thing for now
        ).load()
        SidePlatform(self.name + "_platform", (plat_f1, f2), plat_symmetry, self.internal_category).load()


class HorizontalTriple(Traversable):
    def load(self):
        v = LazyVoxel(
            os.path.basename(self.source),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(self.source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{self.source}.vox": path,
            load_from="station/files/gorender.json",
        )
        self.do_work(v)

    f1x = 6

    def do_work(self, v):
        ground, fake_ground_sprites = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2v.in_place_subset(self.symmetry.render_indices())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1_symmetry = self.symmetry.break_y_symmetry()
        f1v = v.discard_layers(("ground level - platform",), "full")
        f1v.in_place_subset(f1_symmetry.render_indices())
        f1 = f1_symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x))

        plat_f1 = v.discard_layers(("ground level",), "platform")
        plat_f1.in_place_subset(f1_symmetry.render_indices())

        f1s = AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, 0))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height))

        self.register(ALayout(ground, [f1s, f1s.T, f2s], True, notes=["third"]), "")
        self.register(ALayout(ground, [f1s, f2s], True, notes=["third"]), "_third")
        self.register(ALayout(ground, [f1s, f2s, plat_shed.T], True, notes=["third", "far"]), "_third_f")
        SidePlatform(self.name + "_platform", (plat_f1, f2), f1_symmetry, self.internal_category).load()


class SideDouble(LoadType):
    def do_work(self, v):
        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        SideFull(
            self.name,
            (v.discard_layers(("ground level - platform",), "full"), f2),
            self.symmetry,
            self.internal_category,
        ).load()
        SidePlatform(
            self.name + "_platform",
            (v.discard_layers(("ground level",), "platform"), f2),
            self.symmetry,
            self.internal_category,
        ).load()


class SideTriple(LoadType):
    def do_work(self, v):
        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        SideFull(
            self.name,
            (v.discard_layers(("ground level - platform", "ground level - third"), "full"), f2),
            self.symmetry,
            self.internal_category,
        ).load()
        SidePlatform(
            self.name + "_platform",
            (v.discard_layers(("ground level", "ground level - third"), "platform"), f2),
            self.symmetry,
            self.internal_category,
        ).load()
        SideThird(
            self.name + "_third",
            (v.discard_layers(("ground level", "ground level - platform"), "third"), f2),
            self.symmetry,
            self.internal_category,
        ).load()


def quickload(source, type, traversable, groundtype, category):
    worker_class = {
        (True, "central"): TraversablePlatform,
        (True, True): TraversablePlatformSide,
        (True, False): TraversableCorridor,
        (True, "single"): HorizontalSingle,
        (True, "single-1"): HorizontalSingleAsym,
        (True, "double"): HorizontalDouble,
        (True, "triple"): HorizontalTriple,
        (True, "third"): SideThird,
        (False, True): SidePlatform,
        (False, False): SideFull,
        (False, "double"): SideDouble,
        (False, "triple"): SideTriple,
    }[(traversable, groundtype)]

    worker_class(source.split("/")[-1], source, type, category).load()


layouts = []
entries = []
named_tiles = AttrDict()
for name, symmetry, traversable, groundtype, category in [
    ("corner", BuildingSpriteSheetFull, False, "triple", "F1"),
    ("corner_gate", BuildingSpriteSheetFull, False, "triple", "F1"),
    ("corner_2", BuildingSpriteSheetFull, False, "triple", "F1"),
    ("corner_gate_2", BuildingSpriteSheetFull, False, "triple", "F1"),
    ("front_normal", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
    ("front_gate", BuildingSpriteSheetFull, False, False, "F0"),
    ("front_gate_extender", BuildingSpriteSheetSymmetricalX, False, False, "F0"),
    ("central", BuildingSpriteSheetSymmetrical, True, "central", "N"),
    ("central_windowed", BuildingSpriteSheetSymmetricalY, True, "central", "N"),
    ("central_windowed_extender", BuildingSpriteSheetSymmetrical, True, "central", "N"),
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
    ("h_end", BuildingSpriteSheetSymmetricalY, True, "single", "H"),
    ("h_end_asym", BuildingSpriteSheetFull, False, "double", "H"),
    ("h_end_asym_gate", BuildingSpriteSheetFull, False, "triple", "H"),
    ("h_end_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
    ("h_end_gate_1", BuildingSpriteSheetFull, True, "single-1", "H"),
    ("h_normal", BuildingSpriteSheetSymmetrical, True, "triple", "H"),
    ("h_gate", BuildingSpriteSheetSymmetricalY, True, False, "H"),
    ("h_gate_1_platform", BuildingSpriteSheetFull, False, True, "H"),
    ("h_gate_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
    ("h_gate_extender_1_platform", BuildingSpriteSheetFull, False, True, "H"),
    ("h_windowed", BuildingSpriteSheetSymmetricalY, True, False, "H"),
    ("h_windowed_extender", BuildingSpriteSheetSymmetrical, True, False, "H"),
    ("v_end", BuildingSpriteSheetSymmetricalX, False, "triple", "F0"),
    ("v_end_gate", BuildingSpriteSheetSymmetricalX, False, "triple", "F0"),
    ("v_central", BuildingSpriteSheetSymmetrical, True, True, "N"),
    ("tiny", BuildingSpriteSheetSymmetrical, True, "single", "H"),
    ("tiny_asym_platform", BuildingSpriteSheetSymmetricalX, False, True, "H"),
    ("irregular/turn", BuildingSpriteSheetFull, False, False, "T"),
    ("irregular/turn_gate", BuildingSpriteSheetFull, False, False, "T"),
    ("irregular/tee", BuildingSpriteSheetSymmetricalX, False, "double", "T"),
    ("irregular/cross", BuildingSpriteSheetSymmetrical, False, False, "T"),
    ("irregular/double_corner", BuildingSpriteSheetRotational, False, False, "T"),
    ("irregular/funnel", BuildingSpriteSheetFull, False, False, "T"),
    ("irregular/inner_corner", BuildingSpriteSheetFull, False, False, "T"),
    ("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, False, False, "T"),
    ("irregular/v_funnel", BuildingSpriteSheetFull, False, False, "T"),
    ("irregular/v_funnel_2", BuildingSpriteSheetFull, False, False, "T"),
    ("junction/front_corner", BuildingSpriteSheetDiagonal, False, False, "X"),
    ("junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, False, False, "X"),
    ("junction/double_corner_2", BuildingSpriteSheetDiagonal, False, False, "X"),
    ("junction/bicorner", BuildingSpriteSheetDiagonal, False, False, "X"),
    ("junction/bicorner_2", BuildingSpriteSheetDiagonal, False, False, "X"),
]:
    quickload(name, symmetry, traversable, groundtype, category)
