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
    cns_shelter_d as platform,
    cns_shelter as platform_s,
    cns_side_shelter as platform_s_nt,
    concourse as concourse_tile,
    platform_height,
    shelter_height,
    platform_width,
)
from station.stations.ground import named_ps as ground_ps, named_tiles as ground_tiles, gray, gray_third
from station.stations.misc import track_ground, track
from dataclasses import dataclass


base_height = 14
building_height = 48
overpass_height = building_height - base_height

gray_layout = ground_tiles.gray
gray_ps = ground_ps.gray
plat = platform_ps.cns
plat_nt = platform_ps.cns_side
concourse = platform_ps.concourse
third = AChildSprite(gray_third, (0, 0))
third_T = AChildSprite(gray_third.T, (0, 0))


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


@dataclass
class HPos:
    non_platform: ALayout
    platform: ALayout
    platform_back_cut: ALayout


def make_hpos(pillar_style, platform_style):
    return HPos(
        platform_ps["cns_np_pillar" + pillar_style],
        platform_ps["cns" + platform_style],
        platform_ps["cns_cut" + platform_style],
    )


Normal = make_hpos("", "_pillar")
Side = make_hpos("_building", "_shelter_building")
V = make_hpos("", "_shelter_building_v")
TinyAsym = make_hpos("_central", "_pillar_central")


all_f1_layers = (
    "ground level",
    "ground level - platform",
    "ground level - third",
    "ground level - third - t",
    "entrance",
    "entrance - t",
    "pillar",
    "pillar - t",
)
all_f1_layers_set = set(all_f1_layers)


f1_subsets = {
    "third": ({"ground level - third", "entrance", "pillar"}, 16 - platform_width, platform_width),
    "third_t": ({"ground level - third - t", "entrance - t", "pillar - t"}, 0, platform_width),
    "platform": ({"ground level - platform", "entrance", "pillar"}, platform_width, 16 - platform_width),
}


def make_f2(v):
    return v.discard_layers(all_f1_layers, "f2")


def make_f1(v, subset, sym):
    keep_layers, xdiff, xspan = f1_subsets[subset]
    v = v.discard_layers(tuple(all_f1_layers_set - keep_layers), subset)
    v = v.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
    v.in_place_subset(sym.render_indices())
    s = sym.create_variants(v.spritesheet(xdiff=xdiff, xspan=xspan))
    return AParentSprite(s, (16, xspan, base_height), (0, xdiff, platform_height))


def register(l, symmetry, internal_category, name):
    if "y" in l.notes:
        symmetry = symmetry.break_y_symmetry()
    l = symmetry.get_all_variants(l)
    for i, layout in enumerate(l):
        layout.category = get_category(internal_category, i >= len(l) // 2, layout.notes, layout.traversable)
    layouts.extend(l)
    l = symmetry.create_variants(l)
    entries.extend(symmetry.get_all_entries(l))
    named_tiles[name] = l


solid_ground = [gray_ps]
corridor_ground = [track_ground, third, third_T]
one_side_ground = [track_ground, third]


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
        register(l, self.symmetry, self.internal_category, self.name + suffix)


class TraversablePlatform(LoadType):
    def __init__(self, *args, h_pos=Normal, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos

    def get_ground_sprites(self):
        return [track_ground]

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


class SideBase(LoadType):
    def get_ground_sprites(self):
        return [gray_ps]


class TwoFloorMixin:
    def __init__(self, *args, h_pos=Normal, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos

    def get_sprites(self, voxel):
        f1base, f2 = voxel
        f1v = f1base.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        f1 = self.symmetry.create_variants(f1v.spritesheet(xdiff=16 - self.f1x, xspan=self.f1x))
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
            f2v = make_f2(f2base)
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
        self.register(ALayout(grounds, parents + [cur_plat, platform_ps.concourse_side.T], False, notes=["far"]))


class SideThird(TwoFloorMixin, LoadType):
    f1x = platform_width

    def get_ground_sprites(self):
        return one_side_ground

    def make_platform_variants(self, grounds, parents):
        cur_np = self.h_pos.non_platform.T
        cur_plat = self.h_pos.platform.T
        self.register(ALayout(grounds, parents + [cur_np, plat], True, notes=["third"]))
        self.register(ALayout(grounds, parents + [cur_plat, plat_nt], True, notes=["third", "far"]), "_f")


class ALoader(LoadType):
    def __init__(self, *args, h_pos=Normal, force_corridor=False, make_platform=True, full=True, asym=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos
        self.make_platform = make_platform
        self.force_corridor = force_corridor
        self.full = full
        self.asym = asym

    def do_work(self, v):
        cur_np = self.h_pos.non_platform
        cur_plat = self.h_pos.platform

        f2v = make_f2(v)
        f2 = self.symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

        f1_symmetry = self.symmetry.break_y_symmetry()
        f1 = make_f1(v, "third", f1_symmetry)
        if self.asym:
            f1b = make_f1(v, "third_t", f1_symmetry)
        else:
            f1b = f1.T

        plat_f1 = make_f1(v, "platform", f1_symmetry)

        full_f1 = v.discard_layers(
            ("ground level - third", "ground level - third - t", "ground level - platform"), "full"
        )

        f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

        register(
            ALayout(corridor_ground, [plat, plat.T, f1, f1b, f2s], True, notes=["third"]),
            self.symmetry,
            self.internal_category,
            self.name + "_corridor",
        )
        if not self.force_corridor:
            register(
                ALayout(one_side_ground, [plat, f1, cur_np.T, f2s], True, notes=["third", "y"]),
                f1_symmetry,
                self.internal_category,
                self.name + "_third",
            )
            register(
                ALayout(corridor_ground, [plat_nt, f1, cur_plat.T, f2s], True, notes=["third", "y", "far"]),
                f1_symmetry,
                self.internal_category,
                self.name + "_third_f",
            )
        if self.make_platform:
            register(
                ALayout(
                    solid_ground,
                    [plat_f1, f2s, self.h_pos.platform_back_cut.T, platform_ps.concourse_side.T],
                    False,
                    notes=["far"],
                ),
                f1_symmetry,
                self.internal_category,
                self.name + "_platform",
            )
        if self.full:
            SideFull((full_f1, f2), self.symmetry, self.internal_category, name=self.name).load()


class HorizontalSingle(ALoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, make_platform=False, full=False, **kwargs)


class HorizontalTriple(ALoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, full=False, **kwargs)


class SideTriple(LoadType):
    def __init__(self, *args, h_pos=Normal, third=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.h_pos = h_pos
        self.third = third

    def do_work(self, v):
        f2v = make_f2(v)
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
        if self.third:
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
SideFull("h_end_untraversable", BuildingSpriteSheetSymmetricalY, "H").load()
SideTriple("h_end_asym", BuildingSpriteSheetFull, "H", h_pos=Side).load()
SideTriple("h_end_asym_gate", BuildingSpriteSheetFull, "H", h_pos=Side).load()
HorizontalSingle("h_end_gate", BuildingSpriteSheetSymmetricalY, "H", force_corridor=True).load()
SideFull("h_end_gate_untraversable", BuildingSpriteSheetSymmetricalY, "H").load()
ALoader("h_end_gate_1", BuildingSpriteSheetFull, "H", asym=True, make_platform=False, full=False).load()
ALoader("h_normal", BuildingSpriteSheetSymmetrical, "H").load()
ALoader("h_gate", BuildingSpriteSheetSymmetricalY, "H", force_corridor=True, make_platform=False).load()
ALoader("h_gate_1", BuildingSpriteSheetFull, "H", asym=True).load()
ALoader("h_gate_extender", BuildingSpriteSheetSymmetrical, "H", force_corridor=True, make_platform=False).load()
ALoader("h_gate_extender_1", BuildingSpriteSheetSymmetricalX, "H", asym=True).load()
HorizontalTriple("h_windowed", BuildingSpriteSheetSymmetricalY, "H").load()
HorizontalTriple("h_windowed_extender", BuildingSpriteSheetSymmetrical, "H").load()

SideTriple("v_end", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V).load()
SideTriple("v_end_gate", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V).load()
TraversablePlatform("v_central", BuildingSpriteSheetSymmetrical, "N", h_pos=V).load()

HorizontalSingle("tiny", BuildingSpriteSheetSymmetrical, "H", h_pos=V).load()
SideFull("tiny_untraversable", BuildingSpriteSheetSymmetrical, "H").load()
SideTriple("tiny_asym", BuildingSpriteSheetSymmetricalX, "H", h_pos=TinyAsym).load()

SideFull("irregular/turn", BuildingSpriteSheetFull, "T").load()
SideFull("irregular/turn_gate", BuildingSpriteSheetFull, "T").load()
SideTriple("irregular/tee", BuildingSpriteSheetSymmetricalX, "T").load()
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
