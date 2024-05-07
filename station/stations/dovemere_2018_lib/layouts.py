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
    AChildSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platforms import (
    named_ps as platform_ps,
    cnsps_shed_d as platform,
    cnsps_shed as platform_s,
    cnsps_side_shed as platform_s_nt,
    concourse as concourse_tile,
    platform_height,
    shed_height,
    platform_width,
)
from station.stations.ground import named_ps as ground_ps, named_tiles as ground_tiles, gray, gray_third
from station.stations.misc import track_ground, track
from dataclasses import dataclass


gray_layout = ground_tiles.gray
gray_ps = ground_ps.gray


def get_category(internal_category, back, notes, tra):
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
    elif internal_category in ["A", "B", "C", "D", "N", "H", "T"]:
        if internal_category == "N":
            ret = 0x90
        elif internal_category == "H":
            ret = 0xB0
            if tra:
                ret += 0x4
        elif internal_category == "T":
            ret = 0xC0
            if tra:
                ret += 0x4
        else:
            ret = 0xA0 + 0x04 * (ord(internal_category) - ord("A"))
        if "near" in notes:
            ret += 1 ^ (back * 3)
        elif "far" in notes:
            ret += 2 ^ (back * 3)
        elif "both" in notes:
            ret += 3
    elif internal_category == "X":
        ret = 0xF0
    else:
        raise KeyError(f"Unsupported internal category {internal_category}")
    return b"\xe8\x8a\x9c" + ret.to_bytes(1, "little")


base_height = 14
building_height = 48
overpass_height = building_height - base_height
np_pillar = platform_ps.cnsps_np_pillar
np_pillar_building = platform_ps.cnsps_np_pillar_building
np_pillar_central = platform_ps.cnsps_np_pillar_central
plat = platform_ps.cnsps
plat_pillar = platform_ps.cnsps_pillar
plat_pillar_central = platform_ps.cnsps_pillar_central
plat_nt = platform_ps.cnsps_side
plat_nt_pillar = platform_ps.cnsps_side_pillar
plat_nt_pillar_central = platform_ps.cnsps_side_pillar_central
plat_shed = platform_ps.cnsps_shed_building
plat_shed_v = platform_ps.cnsps_shed_building_v
plat_shed_nt = platform_ps.cnsps_side_shed_building
plat_shed_nt_v = platform_ps.cnsps_side_shed_building_v
concourse = platform_ps.concourse
third = AChildSprite(gray_third, (0, 0))
third_T = AChildSprite(gray_third.T, (0, 0))


@dataclass
class HPos:
    non_platform: ALayout
    platform: ALayout
    platform_back: ALayout
    platform_back_cut: ALayout


Normal = HPos(np_pillar, plat_pillar, plat_nt_pillar, platform_ps.cnsps_cut_pillar)
Side = HPos(np_pillar_building, plat_shed, plat_shed_nt, platform_ps.cnsps_cut_shed_building)
V = HPos(np_pillar, plat_shed_v, plat_shed_nt_v, platform_ps.cnsps_cut_shed_building_v)
TinyAsym = HPos(np_pillar_central, plat_pillar_central, plat_nt_pillar_central, platform_ps.cnsps_cut_pillar_central)


class LoadType:
    def __init__(self, source, symmetry, internal_category, name=None):
        self.source = source
        self.symmetry = symmetry
        self.internal_category = internal_category
        self.name = name or source.split("/")[-1]

    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet())
        return [AParentSprite(sprite, (16, 16, building_height), (0, 0, platform_height)), concourse]

    def make_platform_variants(self, grounds, parents):
        self.register(ALayout(grounds, parents, True))

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
        grounds = self.get_ground_sprites()
        sprites = self.get_sprites(v)

        self.make_platform_variants(grounds, sprites)

    def register(self, l, suffix=""):
        if "y" in l.notes:
            cur_sym = self.symmetry.break_y_symmetry()
        else:
            cur_sym = self.symmetry
        l = cur_sym.get_all_variants(l)
        for i, layout in enumerate(l):
            layout.category = get_category(self.internal_category, i >= len(l) // 2, layout.notes, layout.traversable)
        layouts.extend(l)
        l = cur_sym.create_variants(l)
        entries.extend(cur_sym.get_all_entries(l))
        named_tiles[self.name + suffix] = l


class Traversable(LoadType):
    def get_ground_sprites(self):
        return [track_ground]


class TraversablePlatform(Traversable):
    def __init__(self, *args, h_pos=Normal, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos

    def get_sprites(self, voxel):
        sprite = self.symmetry.create_variants(voxel.spritesheet(zdiff=base_height * 2))
        return [AParentSprite(sprite, (16, 16, overpass_height), (0, 0, base_height + platform_height))]

    def make_platform_variants(self, grounds, parents):
        cur_np = self.h_pos.non_platform
        cur_plat = self.h_pos.platform

        if self.symmetry.is_symmetrical_y():
            self.register(ALayout(grounds, parents + [cur_np, cur_np.T], True), "_x")
            self.register(ALayout(grounds, parents + [cur_plat, cur_np.T], True, notes=["y", "near"]), "_n")
            self.register(ALayout(grounds, parents + [cur_plat, cur_plat.T], True, notes=["both"]))
        else:
            self.register(ALayout(grounds, parents + [cur_np, cur_np.T], True), "_x")
            self.register(ALayout(grounds, parents + [cur_plat, cur_np.T], True, notes=["near"]), "_n")
            self.register(ALayout(grounds, parents + [cur_np, cur_plat.T], True, notes=["far"]), "_f")
            self.register(ALayout(grounds, parents + [cur_plat, cur_plat.T], True, notes=["both"]))


class TraversableCorridor(Traversable):
    def get_ground_sprites(self):
        return [track_ground, third, third_T]


class SideBase(LoadType):
    def get_ground_sprites(self):
        return [gray_ps]


class TwoFloorMixin:
    def __init__(self, *args, h_pos=Normal, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos

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
            AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height)),
            AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height)),
        ]


class SideFull(TwoFloorMixin, SideBase):
    f1x = 16

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
            AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height)),
            AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height)),
            concourse,
        ]

    def make_platform_variants(self, grounds, parents):
        self.register(ALayout(grounds, parents, False))


class SidePlatform(TwoFloorMixin, SideBase):
    f1x = 16 - platform_width

    def make_platform_variants(self, grounds, parents):
        cur_plat = self.h_pos.platform_back_cut.T
        self.register(ALayout(grounds, parents + [cur_plat, platform_ps.side_concourse.T], False, notes=["far"]))


class SideThird(TwoFloorMixin, Traversable):
    f1x = platform_width

    def get_ground_sprites(self):
        return [track_ground, third]

    def make_platform_variants(self, grounds, parents):
        cur_np = self.h_pos.non_platform.T
        cur_plat = self.h_pos.platform.T
        self.register(ALayout(grounds, parents + [cur_np, plat_nt], True, notes=["third"]))
        self.register(ALayout(grounds, parents + [cur_plat, plat_nt], True, notes=["third", "far"]), "_f")


class HorizontalSingle(TraversableCorridor):
    def __init__(self, *args, force_corridor=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.force_corridor = force_corridor

    f1x = platform_width

    def do_work(self, v):
        grounds = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1v = v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1_symmetry = self.symmetry.break_y_symmetry()
        f1v.in_place_subset(f1_symmetry.render_indices())
        f1 = f1_symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x))

        f1s = AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

        self.register(ALayout(grounds, [f1s, f1s.T, f2s], True), "")
        if not self.force_corridor:
            self.register(ALayout([track_ground, third], [f1s, np_pillar.T, f2s], True, notes=["third", "y"]), "_third")
            self.register(ALayout(grounds, [f1s, f2s, plat_shed.T], True, notes=["third", "y", "far"]), "_third_f")


class HorizontalSingleAsym(TraversableCorridor):
    f1x = platform_width

    def do_work(self, v):
        grounds = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1v = v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1vb = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/front.vox", "back")
        f1vf = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/back.vox", "front")
        f1_symmetry = self.symmetry.break_y_symmetry()
        f1vb.in_place_subset(f1_symmetry.render_indices())
        f1vf.in_place_subset(f1_symmetry.render_indices())
        f1f = f1_symmetry.create_variants(f1vf.spritesheet(xdiff=16 - self.f1x))
        f1b = f1_symmetry.create_variants(f1vb.spritesheet(xdiff=16 - self.f1x))

        f1fs = AParentSprite(f1f, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f1bs = AParentSprite(f1b, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

        self.register(ALayout(grounds, [f1fs, f1bs, f2s], True), "")
        self.register(ALayout([track_ground, third], [f1fs, np_pillar.T, f2s], True, notes=["third", "y"]), "_third")
        self.register(ALayout(grounds, [f1fs, f2s, plat_shed.T], True, notes=["third", "y", "far"]), "_third_f")


class HorizontalDouble(LoadType):
    def do_work(self, v):
        plat_symmetry = self.symmetry.break_y_symmetry()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2v.in_place_subset(plat_symmetry.render_indices())
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        corridor = v.discard_layers(("ground level - platform",), "full")

        plat_f1 = v.discard_layers(("ground level",), "platform")
        plat_f1.in_place_subset(plat_symmetry.render_indices())

        HorizontalSingle(corridor, self.symmetry, self.internal_category, name=self.name, force_corridor=True).load()
        SidePlatform((plat_f1, f2), plat_symmetry, self.internal_category, name=self.name + "_platform").load()


class HorizontalTriple(TraversableCorridor):
    f1x = platform_width

    def do_work(self, v):
        grounds = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1_symmetry = self.symmetry.break_y_symmetry()
        f1v = v.discard_layers(("ground level - platform",), "full")
        f1v = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1v.in_place_subset(f1_symmetry.render_indices())
        f1 = f1_symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x))

        plat_f1 = v.discard_layers(("ground level",), "platform")
        plat_f1.in_place_subset(f1_symmetry.render_indices())

        f1s = AParentSprite(f1, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

        self.register(ALayout(grounds, [f1s, f1s.T, f2s], True, notes=["third"]), "")
        self.register(ALayout(grounds, [f1s, np_pillar.T, f2s], True, notes=["third", "y"]), "_third")
        self.register(ALayout(grounds, [f1s, f2s, plat_pillar.T], True, notes=["third", "y", "far"]), "_third_f")
        SidePlatform((plat_f1, f2), f1_symmetry, self.internal_category, name=self.name + "_platform").load()


class HorizontalTripleAsym(TraversableCorridor):
    f1x = platform_width

    def do_work(self, v):
        grounds = self.get_ground_sprites()

        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1_symmetry = self.symmetry.break_y_symmetry()
        f1v = v.discard_layers(("ground level - platform",), "full")

        plat_f1 = v.discard_layers(("ground level",), "platform")
        plat_f1.in_place_subset(f1_symmetry.render_indices())

        f1v = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1vb = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/front.vox", "back")
        f1vf = f1v.mask_clip_away("station/voxels/dovemere_2018/masks/back.vox", "front")
        f1_symmetry = self.symmetry.break_y_symmetry()
        f1vb.in_place_subset(f1_symmetry.render_indices())
        f1vf.in_place_subset(f1_symmetry.render_indices())
        f1f = f1_symmetry.create_variants(f1vf.spritesheet(xdiff=16 - self.f1x))
        f1b = f1_symmetry.create_variants(f1vb.spritesheet(xdiff=16 - self.f1x))

        f1fs = AParentSprite(f1f, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f1bs = AParentSprite(f1b, (16, self.f1x, base_height), (0, 16 - self.f1x, platform_height))
        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

        self.register(ALayout(grounds, [f1fs, f1bs, f2s], True), "")
        self.register(ALayout([track_ground, third], [f1fs, np_pillar.T, f2s], True, notes=["third", "y"]), "_third")
        self.register(ALayout(grounds, [f1fs, plat_pillar.T, f2s], True, notes=["third", "y", "far"]), "_third_f")
        SidePlatform((plat_f1, f2), f1_symmetry, self.internal_category, name=self.name + "_platform").load()


class SideDouble(LoadType):
    def do_work(self, v):
        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        SideFull(
            (v.discard_layers(("ground level - platform",), "full"), f2),
            self.symmetry,
            self.internal_category,
            name=self.name,
        ).load()
        SidePlatform(
            (v.discard_layers(("ground level",), "platform"), f2),
            self.symmetry,
            self.internal_category,
            name=self.name + "_platform",
        ).load()


class SideTriple(LoadType):
    def __init__(self, *args, h_pos=Normal, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos

    def do_work(self, v):
        f2v = v.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))
        SideFull(
            (v.discard_layers(("ground level - platform", "ground level - third"), "full"), f2),
            self.symmetry,
            self.internal_category,
            name=self.name,
        ).load()
        SidePlatform(
            (v.discard_layers(("ground level", "ground level - third"), "platform"), f2),
            self.symmetry,
            self.internal_category,
            name=self.name + "_platform",
            h_pos=self.h_pos,
        ).load()
        SideThird(
            (v.discard_layers(("ground level", "ground level - platform"), "third"), f2),
            self.symmetry,
            self.internal_category,
            name=self.name + "_third",
            h_pos=self.h_pos,
        ).load()


layouts = []
entries = []
flexible_entries = []
named_tiles = AttrDict()

SideTriple("front_normal", BuildingSpriteSheetSymmetricalX, "F0").load()
SideTriple("front_gate", BuildingSpriteSheetFull, "F0").load()
SideTriple("front_gate_extender", BuildingSpriteSheetSymmetricalX, "F0").load()

SideTriple("corner", BuildingSpriteSheetFull, "F1", h_pos=Side).load()
SideTriple("corner_gate", BuildingSpriteSheetFull, "F1", h_pos=Side).load()
SideTriple("corner_2", BuildingSpriteSheetFull, "F1", h_pos=Side).load()
SideTriple("corner_gate_2", BuildingSpriteSheetFull, "F1", h_pos=Side).load()

TraversablePlatform("central", BuildingSpriteSheetSymmetrical, "N").load()
TraversablePlatform("central_windowed", BuildingSpriteSheetSymmetricalY, "N").load()
TraversablePlatform("central_windowed_extender", BuildingSpriteSheetSymmetrical, "N").load()

TraversablePlatform("side_a", BuildingSpriteSheetFull, "A", h_pos=Side).load()
TraversablePlatform("side_a_windowed", BuildingSpriteSheetFull, "A", h_pos=Side).load()
TraversablePlatform("side_a2", BuildingSpriteSheetSymmetricalY, "A", h_pos=Side).load()
TraversablePlatform("side_a2_windowed", BuildingSpriteSheetSymmetricalY, "A", h_pos=Side).load()
TraversablePlatform("side_a3", BuildingSpriteSheetFull, "A", h_pos=Side).load()
TraversablePlatform("side_a3_windowed", BuildingSpriteSheetFull, "A", h_pos=Side).load()
TraversablePlatform("side_b", BuildingSpriteSheetFull, "B", h_pos=Side).load()
TraversablePlatform("side_b2", BuildingSpriteSheetSymmetricalY, "B", h_pos=Side).load()
TraversablePlatform("side_c", BuildingSpriteSheetSymmetricalY, "C", h_pos=Side).load()
TraversablePlatform("side_d", BuildingSpriteSheetSymmetricalY, "D", h_pos=Side).load()

HorizontalSingle("h_end", BuildingSpriteSheetSymmetricalY, "H").load()
SideTriple("h_end_asym", BuildingSpriteSheetFull, "H", h_pos=Side).load()
SideTriple("h_end_asym_gate", BuildingSpriteSheetFull, "H", h_pos=Side).load()
HorizontalSingle("h_end_gate", BuildingSpriteSheetSymmetricalY, "H", force_corridor=True).load()
HorizontalSingleAsym("h_end_gate_1", BuildingSpriteSheetFull, "H").load()
HorizontalTriple("h_normal", BuildingSpriteSheetSymmetrical, "H").load()
HorizontalSingle("h_gate", BuildingSpriteSheetSymmetricalY, "H", force_corridor=True).load()
HorizontalTripleAsym("h_gate_1", BuildingSpriteSheetFull, "H").load()
HorizontalSingle("h_gate_extender", BuildingSpriteSheetSymmetrical, "H", force_corridor=True).load()
HorizontalTripleAsym("h_gate_extender_1", BuildingSpriteSheetSymmetricalX, "H").load()
HorizontalSingle("h_windowed", BuildingSpriteSheetSymmetricalY, "H", force_corridor=True).load()
HorizontalSingle("h_windowed_extender", BuildingSpriteSheetSymmetrical, "H", force_corridor=True).load()

SideTriple("v_end", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V).load()
SideTriple("v_end_gate", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V).load()
TraversablePlatform("v_central", BuildingSpriteSheetSymmetrical, "N", h_pos=V).load()

HorizontalSingle("tiny", BuildingSpriteSheetSymmetrical, "H").load()
SideTriple("tiny_asym", BuildingSpriteSheetSymmetricalX, "H", h_pos=TinyAsym).load()

SideFull("irregular/turn", BuildingSpriteSheetFull, "T").load()
SideFull("irregular/turn_gate", BuildingSpriteSheetFull, "T").load()
SideDouble("irregular/tee", BuildingSpriteSheetSymmetricalX, "T").load()
SideFull("irregular/cross", BuildingSpriteSheetSymmetrical, "T").load()
SideFull("irregular/double_corner", BuildingSpriteSheetRotational, "T").load()
SideTriple("irregular/funnel", BuildingSpriteSheetFull, "T").load()
SideFull("irregular/inner_corner", BuildingSpriteSheetFull, "T").load()
SideFull("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, "T").load()
SideFull("irregular/v_funnel", BuildingSpriteSheetFull, "T").load()
SideFull("irregular/v_funnel_2", BuildingSpriteSheetFull, "T").load()

SideFull("junction/front_corner", BuildingSpriteSheetDiagonal, "X").load()
SideFull("junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, "X").load()
SideFull("junction/double_corner_2", BuildingSpriteSheetDiagonal, "X").load()
SideFull("junction/bicorner", BuildingSpriteSheetDiagonal, "X").load()
SideFull("junction/bicorner_2", BuildingSpriteSheetDiagonal, "X").load()
