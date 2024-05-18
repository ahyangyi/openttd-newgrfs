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
    "full": ({"ground level", "entrance", "pillar", "entrance - t", "pillar - t"}, 0, 16),
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


def load(
    source,
    symmetry,
    internal_category,
    name=None,
    h_pos=Normal,
    corridor=True,
    third=True,
    platform=True,
    full=True,
    asym=False,
):
    name = name or source.split("/")[-1]
    v = LazyVoxel(
        os.path.basename(source),
        prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(source)),
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/{source}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
    )
    f2v = make_f2(v)
    f2 = symmetry.create_variants(f2v.spritesheet(zdiff=base_height * 2))

    f1_symmetry = symmetry.break_y_symmetry()
    f1 = make_f1(v, "third", f1_symmetry)
    if asym:
        f1b = make_f1(v, "third_t", f1_symmetry)
    else:
        f1b = f1.T

    plat_f1 = make_f1(v, "platform", f1_symmetry)
    full_f1 = make_f1(v, "full", symmetry)

    f2s = AParentSprite(f2, (16, 16, overpass_height), (0, 0, base_height + platform_height))

    if corridor:
        register(
            ALayout(corridor_ground, [plat, plat.T, f1, f1b, f2s], True, notes=["third"]),
            symmetry,
            internal_category,
            name + "_corridor",
        )
    if third:
        register(
            ALayout(one_side_ground, [plat, f1, h_pos.non_platform.T, f2s], True, notes=["third", "y"]),
            f1_symmetry,
            internal_category,
            name + "_third",
        )
        register(
            ALayout(corridor_ground, [plat_nt, f1, h_pos.platform.T, f2s], True, notes=["third", "y", "far"]),
            f1_symmetry,
            internal_category,
            name + "_third_f",
        )
    if platform:
        register(
            ALayout(
                solid_ground,
                [plat_f1, f2s, h_pos.platform_back_cut.T, platform_ps.concourse_side.T],
                False,
                notes=["far"],
            ),
            f1_symmetry,
            internal_category,
            name + "_platform",
        )
    if full:
        register(ALayout(solid_ground, [full_f1, f2s, concourse], False), symmetry, internal_category, name)


def load_full(source, symmetry, internal_category, name=None, h_pos=Normal):
    load(source, symmetry, internal_category, name=name, h_pos=h_pos, corridor=False, third=False, platform=False)


layouts = []
entries = []
flexible_entries = []
named_tiles = AttrDict()

load("front_normal", BuildingSpriteSheetSymmetricalX, "F0", corridor=False)
load("front_gate", BuildingSpriteSheetFull, "F0", corridor=False)
load("front_gate_extender", BuildingSpriteSheetSymmetricalX, "F0", corridor=False)

load("corner", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)
load("corner_gate", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)
load("corner_2", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)
load("corner_gate_2", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)

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

load("h_end", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False)
load_full("h_end_untraversable", BuildingSpriteSheetSymmetricalY, "H")
load("h_end_asym", BuildingSpriteSheetFull, "H", h_pos=Side, corridor=False)
load("h_end_asym_gate", BuildingSpriteSheetFull, "H", h_pos=Side, corridor=False)
load("h_end_gate", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False, third=False)
load_full("h_end_gate_untraversable", BuildingSpriteSheetSymmetricalY, "H")
load("h_end_gate_1", BuildingSpriteSheetFull, "H", asym=True, platform=False, full=False)
load("h_normal", BuildingSpriteSheetSymmetrical, "H")
load("h_gate", BuildingSpriteSheetSymmetricalY, "H", third=False, platform=False)
load("h_gate_1", BuildingSpriteSheetFull, "H", asym=True)
load("h_gate_extender", BuildingSpriteSheetSymmetrical, "H", third=False, platform=False)
load("h_gate_extender_1", BuildingSpriteSheetSymmetricalX, "H", asym=True)
load("h_windowed", BuildingSpriteSheetSymmetricalY, "H")
load("h_windowed_extender", BuildingSpriteSheetSymmetrical, "H")

load("v_end", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V, corridor=False)
load("v_end_gate", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V, corridor=False)
TraversablePlatform("v_central", BuildingSpriteSheetSymmetrical, "N", h_pos=V).load()

load("tiny", BuildingSpriteSheetSymmetrical, "H", h_pos=V, full=False, platform=False)
load_full("tiny_untraversable", BuildingSpriteSheetSymmetrical, "H")
load("tiny_asym", BuildingSpriteSheetSymmetricalX, "H", h_pos=TinyAsym, corridor=False)

load_full("irregular/turn", BuildingSpriteSheetFull, "T")
load_full("irregular/turn_gate", BuildingSpriteSheetFull, "T")
load("irregular/tee", BuildingSpriteSheetSymmetricalX, "T", corridor=False)
load_full("irregular/cross", BuildingSpriteSheetSymmetrical, "T")
load_full("irregular/double_corner", BuildingSpriteSheetRotational, "T")
load("irregular/funnel", BuildingSpriteSheetFull, "T", corridor=False)
load_full("irregular/inner_corner", BuildingSpriteSheetFull, "T")
load_full("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, "T")
load_full("irregular/v_funnel", BuildingSpriteSheetFull, "T")
load_full("irregular/v_funnel_2", BuildingSpriteSheetFull, "T")

load_full("junction/front_corner", BuildingSpriteSheetDiagonal, "X")
load_full("junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, "X")
load_full("junction/double_corner_2", BuildingSpriteSheetDiagonal, "X")
load_full("junction/bicorner", BuildingSpriteSheetDiagonal, "X")
load_full("junction/bicorner_2", BuildingSpriteSheetDiagonal, "X")
