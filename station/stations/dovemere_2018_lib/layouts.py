import os
from station.lib import (
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
    BuildingSpriteSheetRotational,
    BuildingSpriteSheetDiagonal,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platforms import (
    named_ps as platform_ps,
    cns_shelter_1_d as platform_d,
    cns_shelter_1 as platform_n,
    cns_side_shelter_1 as platform_s_nt,
    concourse as concourse_tile,
    platform_height,
    shelter_height,
    platform_width,
    platform_classes,
    shelter_classes,
)
from station.stations.ground import named_ps as ground_ps, named_tiles as ground_tiles, gray, gray_third
from station.stations.misc import track_ground, track
from agrf.graphics.recolour import PROCESS_COLOUR
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
    platform: None
    platform_back_cut: None
    has_shelter: bool


def make_hpos(pillar_style, platform_style):
    return HPos(
        platform_ps["cns_np_pillar" + pillar_style],
        lambda p="concrete", x="shelter_1": platform_ps[
            "cns" + ("" if p == "concrete" else "_" + p) + platform_style.replace("shelter", x)
        ],
        lambda x="shelter_1": platform_ps["cns_cut" + platform_style.replace("shelter", x)],
        "shelter" in platform_style,
    )


Normal = make_hpos("", "_pillar")
Side = make_hpos("_building", "_shelter_building")
V = make_hpos("", "_shelter_building_v")
TinyAsym = make_hpos("_central", "_pillar_central")


all_f2_layers = ("window", "window-extender", "snow", "snow-window", "snow-window-extender")
all_f2_layers_set = set(all_f2_layers)


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


def make_f2(v, sym):
    v = v.discard_layers(all_f1_layers + all_f2_layers, "f2")
    v.in_place_subset(sym.render_indices())
    s = sym.create_variants(v.spritesheet(zdiff=base_height * 2))
    return AParentSprite(s, (16, 16, overpass_height), (0, 0, base_height + platform_height))


def make_f2_extra(v, sym, name):
    if name == "window":
        sym = sym.break_x_symmetry()
    if "snow" in name:
        zbase = base_height + overpass_height + 1
    else:
        zbase = base_height + overpass_height
    v2 = v.discard_layers(all_f1_layers + all_f2_layers, "f2")
    v = v.discard_layers(
        all_f1_layers + tuple(all_f2_layers_set - {name}) + ("overpass", "foundation", "circle"), f"f2_{name}"
    )
    v = v.compose(v2, "merge", ignore_mask=True, colour_map=PROCESS_COLOUR)
    v.config["agrf_palette"] = "station/files/ttd_palette_window.json"
    v.in_place_subset(sym.render_indices())
    s = sym.create_variants(v.spritesheet(zdiff=zbase * 2))
    return AParentSprite(s, (16, 16, 1), (0, 0, zbase + platform_height))


f1_cache = {}


def make_f1(v, subset, sym):
    if (v, subset) not in f1_cache:
        keep_layers, xdiff, xspan = f1_subsets[subset]
        V = v.discard_layers(tuple(all_f1_layers_set - keep_layers), subset)
        V = V.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        V.in_place_subset(sym.render_indices())
        s = sym.create_variants(V.spritesheet(xdiff=xdiff, xspan=xspan))
        f1_cache[(v, subset)] = AParentSprite(s, (16, xspan, base_height), (0, xdiff, platform_height)), sym
    ret, ret_sym = f1_cache[(v, subset)]
    assert sym is ret_sym
    return ret


def register(l, symmetry, internal_category, name):
    l = symmetry.get_all_variants(l)
    for i, layout in enumerate(l):
        layout.category = get_category(internal_category, i >= len(l) // 2, layout.notes, layout.traversable)
    layouts.extend(l)
    l = symmetry.create_variants(l)
    entries.extend(symmetry.get_all_entries(l))
    named_tiles[name] = l


solid_ground = [gray_ps]
corridor_ground = [track_ground + third + third_T]
one_side_ground = [track_ground + third]
one_side_ground_t = [track_ground + third_T]
empty_ground = [track_ground]

voxel_cache = {}


def make_voxel(source):
    if source not in voxel_cache:
        voxel_cache[source] = LazyVoxel(
            os.path.basename(source),
            prefix=os.path.join("station/voxels/render/dovemere_2018", os.path.dirname(source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{source}.vox": path,
            load_from="station/files/gorender.json",
        )
    return voxel_cache[source]


def load_central(source, symmetry, internal_category, name=None, h_pos=Normal, window=None):
    name = name or source.split("/")[-1]
    v = make_voxel(source)
    f2 = make_f2(v, symmetry)
    f2_window = make_f2_extra(v, symmetry, "window")
    f2_window_extender = make_f2_extra(v, symmetry, "window-extender")

    cur_np = h_pos.non_platform
    if window is None:
        window_classes = ["windowed"]
    else:
        window_classes = ["none"] + window
    for window_class in window_classes:
        window_postfix = "" if window_class == "none" else "_" + window_class
        if window is None:
            f2_name = name
        elif window_postfix != "" and name.endswith("_normal"):
            f2_name = name[:-7] + window_postfix
        else:
            f2_name = name + window_postfix
        if window_class == "none":
            f2_component = [f2]
            cur_sym = symmetry
        elif window_class == "windowed":
            f2_component = [f2, f2_window]
            cur_sym = symmetry.break_x_symmetry()
        elif window_class == "windowed_extender":
            f2_component = [f2, f2_window_extender]
            cur_sym = symmetry.break_x_symmetry()
        register(
            ALayout(empty_ground, [cur_np, cur_np.T] + f2_component, True),
            cur_sym,
            internal_category,
            f2_name + "_empty",
        )
        for shelter_class in shelter_classes if h_pos.has_shelter else ["shelter_1"]:
            for platform_class in platform_classes:
                cur_plat = h_pos.platform(platform_class, shelter_class)
                shelter_postfix = "" if shelter_class == "shelter_1" else "_" + shelter_class
                platform_postfix = "" if platform_class == "concrete" else "_" + platform_class
                sname = f2_name + platform_postfix + shelter_postfix
                register(
                    ALayout(corridor_ground, [cur_plat, cur_plat.T] + f2_component, True, notes=["both"]),
                    cur_sym,
                    internal_category,
                    sname + "_d",
                )
                if symmetry.is_symmetrical_y():
                    broken_symmetry = cur_sym.break_y_symmetry()
                    register(
                        ALayout(one_side_ground, [cur_plat, cur_np.T] + f2_component, True, notes=["near"]),
                        broken_symmetry,
                        internal_category,
                        sname + "_n",
                    )
                    named_tiles[sname + "_f"] = named_tiles[sname + "_n"].T
                else:
                    register(
                        ALayout(one_side_ground, [cur_plat, cur_np.T] + f2_component, True, notes=["near"]),
                        cur_sym,
                        internal_category,
                        sname + "_n",
                    )
                    register(
                        ALayout(one_side_ground_t, [cur_np, cur_plat.T] + f2_component, True, notes=["far"]),
                        cur_sym,
                        internal_category,
                        sname + "_f",
                    )


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
    borrow_f1=None,
    borrow_f1_symmetry=BuildingSpriteSheetSymmetrical,
    window=None,
):
    name = name or source.split("/")[-1]
    v = make_voxel(source)
    f2 = make_f2(v, symmetry)
    f2_window = make_f2_extra(v, symmetry, "window")
    f2_window_extender = make_f2_extra(v, symmetry, "window-extender")
    f2_snow = make_f2_extra(v, symmetry, "snow")

    if borrow_f1 is not None:
        v = make_voxel(borrow_f1)
        f1_symmetry = borrow_f1_symmetry
    else:
        f1_symmetry = symmetry
    broken_f1_symmetry = f1_symmetry.break_y_symmetry()
    broken_symmetry = symmetry.break_y_symmetry()
    f1 = make_f1(v, "third", broken_f1_symmetry)
    f1b = make_f1(v, "third_t", broken_f1_symmetry) if asym else f1.T
    plat_f1 = make_f1(v, "platform", broken_f1_symmetry)
    full_f1 = make_f1(v, "full", f1_symmetry)

    if window is None:
        window_classes = ["windowed"]
    else:
        window_classes = ["none"] + window

    for window_class in window_classes:
        window_postfix = "" if window_class == "none" else "_" + window_class
        if window is None:
            f2_name = name
        elif window_postfix != "" and name.endswith("_normal"):
            f2_name = name[:-7] + window_postfix
        else:
            f2_name = name + window_postfix
        if window_class == "none":
            f2_component = [f2, f2_snow]
            cur_sym = symmetry
            cur_bsym = broken_symmetry
        elif window_class == "windowed":
            f2_component = [f2, f2_window, f2_snow]
            cur_sym = symmetry.break_x_symmetry()
            cur_bsym = broken_symmetry.break_x_symmetry()
        elif window_class == "windowed_extender":
            f2_component = [f2, f2_window_extender, f2_snow]
            cur_sym = symmetry
            cur_bsym = broken_symmetry
        for platform_class in platform_classes:
            platform_postfix = "" if platform_class == "concrete" else "_" + platform_class
            cur_plat = platform_ps["cns" + platform_postfix]
            cur_plat_nt = platform_ps["cns" + platform_postfix + "_side"]
            pname = f2_name + platform_postfix
            if corridor:
                register(
                    ALayout(corridor_ground, [cur_plat, cur_plat.T, f1, f1b] + f2_component, True, notes=["third"]),
                    cur_sym,
                    internal_category,
                    pname + "_corridor",
                )
            if third:
                register(
                    ALayout(
                        one_side_ground, [cur_plat, f1, h_pos.non_platform.T] + f2_component, True, notes=["third"]
                    ),
                    cur_bsym,
                    internal_category,
                    pname + "_third",
                )
            for shelter_class in shelter_classes if h_pos.has_shelter else ["shelter_1"]:
                shelter_postfix = "" if shelter_class == "shelter_1" else "_" + shelter_class
                sname = pname + shelter_postfix
                if third:
                    register(
                        ALayout(
                            corridor_ground,
                            [cur_plat_nt, f1, h_pos.platform(platform_class, shelter_class).T] + f2_component,
                            True,
                            notes=["third", "far"],
                        ),
                        cur_bsym,
                        internal_category,
                        sname + "_third_f",
                    )
                if platform:
                    register(
                        ALayout(
                            solid_ground,
                            [
                                plat_f1,
                                h_pos.platform_back_cut(shelter_class).T,
                                platform_ps[f"concourse{platform_postfix}_side"].T,
                            ]
                            + f2_component,
                            False,
                            notes=["far"],
                        ),
                        cur_bsym,
                        internal_category,
                        sname + "_platform",
                    )
        if full:
            register(
                ALayout(solid_ground, [full_f1, concourse] + f2_component, False), cur_sym, internal_category, f2_name
            )


def load_full(source, symmetry, internal_category, name=None, h_pos=Normal, borrow_f1=None, window=None):
    load(
        source,
        symmetry,
        internal_category,
        name=name,
        h_pos=h_pos,
        borrow_f1=borrow_f1,
        corridor=False,
        third=False,
        platform=False,
        window=window,
    )


layouts = []
entries = []
flexible_entries = []
named_tiles = AttrDict()

load("front_normal", BuildingSpriteSheetSymmetricalX, "F0", corridor=False, window=[])
load("front_gate", BuildingSpriteSheetFull, "F0", corridor=False)
load("front_gate_extender", BuildingSpriteSheetSymmetricalX, "F0", corridor=False)

load("corner", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False, window=[])
load("corner_gate", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)
load("corner_2", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False, window=[])
load("corner_gate_2", BuildingSpriteSheetFull, "F1", h_pos=Side, corridor=False)

load_central("central", BuildingSpriteSheetSymmetrical, "N", window=["windowed", "windowed_extender"])

load_central("side_a", BuildingSpriteSheetFull, "A", h_pos=Side, window=["windowed"])
load_central("side_a2", BuildingSpriteSheetSymmetricalY, "A", h_pos=Side, window=["windowed"])
load_central("side_a3", BuildingSpriteSheetFull, "A", h_pos=Side, window=["windowed"])
load_central("side_b", BuildingSpriteSheetFull, "B", h_pos=Side, window=[])
load_central("side_b2", BuildingSpriteSheetSymmetricalY, "B", h_pos=Side, window=[])
load_central("side_c", BuildingSpriteSheetSymmetricalY, "C", h_pos=Side, window=[])
load_central("side_d", BuildingSpriteSheetSymmetricalY, "D", h_pos=Side)

load("h_end", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False, window=[])
load_full("h_end_untraversable", BuildingSpriteSheetSymmetricalY, "H", window=[])
load("h_end_asym", BuildingSpriteSheetFull, "H", h_pos=Side, corridor=False, window=[])
load("h_end_asym_gate", BuildingSpriteSheetFull, "H", h_pos=Side, corridor=False)
load("h_end_gate", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False, third=False)
load_full("h_end_gate_untraversable", BuildingSpriteSheetSymmetricalY, "H")
load("h_end_gate_1", BuildingSpriteSheetFull, "H", asym=True, platform=False, full=False)
load("h_normal", BuildingSpriteSheetSymmetrical, "H", window=["windowed", "windowed_extender"])
load("h_gate", BuildingSpriteSheetSymmetricalY, "H", third=False, platform=False)
load("h_gate_1", BuildingSpriteSheetFull, "H", asym=True)
load("h_gate_extender", BuildingSpriteSheetSymmetrical, "H", third=False, platform=False)
load("h_gate_extender_1", BuildingSpriteSheetSymmetricalX, "H", asym=True)

load("v_end", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V, corridor=False)
load("v_end_gate", BuildingSpriteSheetSymmetricalX, "F0", h_pos=V, corridor=False)
load_central("v_central", BuildingSpriteSheetSymmetrical, "N", h_pos=V)

load("tiny", BuildingSpriteSheetSymmetrical, "H", h_pos=V, full=False, platform=False)
load_full("tiny_untraversable", BuildingSpriteSheetSymmetrical, "H")
load("tiny_asym", BuildingSpriteSheetSymmetricalX, "H", h_pos=TinyAsym, corridor=False)

load_full("irregular/turn", BuildingSpriteSheetFull, "T")
load_full("irregular/turn_gate", BuildingSpriteSheetFull, "T")
load("irregular/tee", BuildingSpriteSheetSymmetricalX, "T", corridor=False, borrow_f1="h_normal")
load("irregular/cross", BuildingSpriteSheetSymmetrical, "T", platform=False, full=False, borrow_f1="h_normal")
load_full("irregular/double_corner", BuildingSpriteSheetRotational, "T", borrow_f1="h_normal", window=[])
load("irregular/funnel", BuildingSpriteSheetFull, "T", corridor=False, borrow_f1="h_normal", window=[])
load_full("irregular/inner_corner", BuildingSpriteSheetFull, "T", window=[])
load_full("irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, "T", borrow_f1="h_normal")
load_full("irregular/v_funnel", BuildingSpriteSheetFull, "T")
load_full("irregular/v_funnel_2", BuildingSpriteSheetFull, "T")

load_full("junction/front_corner", BuildingSpriteSheetDiagonal, "X", window=[])
load_full("junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, "X")
load_full("junction/double_corner_2", BuildingSpriteSheetDiagonal, "X", window=[])
load_full("junction/bicorner", BuildingSpriteSheetDiagonal, "X", window=[])
load_full("junction/bicorner_2", BuildingSpriteSheetDiagonal, "X", window=[])
