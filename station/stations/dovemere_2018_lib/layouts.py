import os
import inspect
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
    Registers,
)
from agrf.graphics.voxel import LazyVoxel
from station.stations.platforms import (
    platform_ps,
    concourse_ps,
    platform_height,
    shelter_height,
    platform_width,
    platform_classes,
    shelter_classes,
    platform_tiles,
    two_side_tiles,
    concourse_tiles,
)
from station.stations.ground import named_ps as ground_ps, named_tiles as ground_tiles, gray, gray_third
from station.stations.misc import track_ground, track
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from dataclasses import dataclass


base_height = 14
building_height = 48
overpass_height = building_height - base_height

gray_layout = ground_tiles.gray
gray_ps = ground_ps.gray
concourse = concourse_ps.none
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
    pillar_style: str
    shelter_style: str
    platform_style: str
    has_shelter: bool
    has_narrow: bool = False

    @property
    def non_platform(self):
        return platform_ps[("cns", "np", "", "pillar", self.pillar_style)]

    def platform(self, p, x):
        return platform_ps[("cns", p, "", x if self.has_shelter else self.shelter_style, self.platform_style)]

    def platform_back_cut(self, x):
        if self.has_narrow:
            return platform_ps[
                ("cns", "cut", "", x if self.has_shelter else self.shelter_style, self.platform_style + "_narrow")
            ]
        else:
            return platform_ps[("cns", "cut", "", x if self.has_shelter else self.shelter_style, self.platform_style)]


Normal = HPos("", "pillar", "", False)
Side = HPos("building", "", "building", True)
SideNarrow = HPos("building", "", "building", True, True)
V = HPos("", "", "building_v", True)
VNarrow = HPos("", "", "building_v", True, True)
TinyAsym = HPos("central", "pillar", "central", False)


snow_layers = ("snow", "snow-window", "snow-window-extender")
all_f2_layers = ("window", "window-extender")
all_f2_layers_set = set(all_f2_layers + snow_layers)


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
all_f1_layers_set = set(all_f1_layers + snow_layers)


f1_subsets = {
    "third": ({"ground level - third", "entrance", "pillar"}, 16 - platform_width, platform_width),
    "third_t": ({"ground level - third - t", "entrance - t", "pillar - t"}, 0, platform_width),
    "platform": ({"ground level - platform", "entrance", "pillar"}, platform_width, 16 - platform_width),
    "full": ({"ground level", "entrance", "pillar", "entrance - t", "pillar - t"}, 0, 16),
}


def make_f2(v, sym):
    v = v.discard_layers(all_f1_layers + all_f2_layers + snow_layers, "f2")
    v.in_place_subset(sym.render_indices())
    v.config["agrf_manual_crop"] = (0, 10)
    s = sym.create_variants(v.spritesheet(zdiff=base_height * 2 + 1))
    return AParentSprite(s, (16, 16, overpass_height), (0, 0, base_height + platform_height))


def make_extra(v, sym, name, floor="f2"):
    vd = v.discard_layers(
        all_f1_layers + tuple(all_f2_layers_set - {name}) + ("overpass", "foundation", "circle"), name
    )
    if floor == "f2":
        vd = vd.mask_clip_away("station/voxels/dovemere_2018/masks/ground_level.vox", "f2")
    else:
        vd = vd.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
    v = vd.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    if "snow" in name:
        v.config["overlap"] = 1.3
    else:
        v.config["agrf_palette"] = "station/files/ttd_palette_window.json"
    if floor == "f2":
        v.config["agrf_childsprite"] = (0, -10)
    else:
        v.config["agrf_childsprite"] = (0, -40)
    v.in_place_subset(sym.render_indices())
    s = sym.create_variants(v.spritesheet())
    if "snow" in name:
        return AChildSprite(s, (0, 0), flags={"dodraw": Registers.SNOW})
    else:
        return AChildSprite(s, (0, 0))


f1_cache = {}


def make_f1(v, subset, sym):
    if (v, subset) not in f1_cache:
        keep_layers, xdiff, xspan = f1_subsets[subset]
        V = v.discard_layers(tuple(all_f1_layers_set - keep_layers), subset)
        V = V.mask_clip_away("station/voxels/dovemere_2018/masks/overpass.vox", "f1")
        V.in_place_subset(sym.render_indices())
        V.config["agrf_manual_crop"] = (0, 40)
        s = sym.create_variants(V.spritesheet(xdiff=xdiff, xspan=xspan, zdiff=1))
        f1_cache[(v, subset)] = AParentSprite(s, (16, xspan, base_height), (0, xdiff, platform_height)), sym
    ret, ret_sym = f1_cache[(v, subset)]
    assert sym is ret_sym
    return ret


def register(base_id, step_id, l, symmetry, internal_category, name):
    l = symmetry.get_all_variants(l)
    for i, layout in enumerate(l):
        layout.category = get_category(internal_category, i >= len(l) // 2, layout.notes, layout.traversable)
    layouts.extend(l)
    l = symmetry.create_variants(l)
    for i, entry in enumerate(symmetry.get_all_entries(l)):
        entry.id = base_id + step_id * i
        entries.append(entry)
    named_tiles[name] = l


solid_ground = gray_ps
corridor_ground = track_ground + third + third_T
one_side_ground = track_ground + third
one_side_ground_t = track_ground + third_T
empty_ground = track_ground

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


def load_central(f2_id, source, symmetry, internal_category, name=None, h_pos=Normal, window=None, window_asym=False):
    name = name or source.split("/")[-1]
    v = make_voxel(source)
    f2 = make_f2(v, symmetry)
    f2_window = make_extra(v, symmetry.break_x_symmetry() if window_asym else symmetry, "window")
    f2_window_extender = make_extra(v, symmetry, "window-extender")
    f2_snow = make_extra(v, symmetry, "snow")
    f2_snow_window = make_extra(v, symmetry.break_x_symmetry() if window_asym else symmetry, "snow-window")
    f2_snow_window_extender = make_extra(v, symmetry, "snow-window-extender")

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
            f2_component = [f2 + f2_snow]
            cur_sym = symmetry
        elif window_class == "windowed":
            f2_component = [f2 + f2_window + f2_snow_window]
            cur_sym = symmetry.break_x_symmetry()
            if window_asym:
                cur_sym = symmetry.break_x_symmetry()
            else:
                cur_sym = symmetry
        elif window_class == "windowed_extender":
            f2_component = [f2 + f2_window_extender + f2_snow_window_extender]
            cur_sym = symmetry
        register(
            0xFD00 + f2_id,
            1,
            ALayout(empty_ground, [cur_np, cur_np.T] + f2_component, True, notes=["waypoint"]),
            cur_sym,
            internal_category,
            (f2_name, None, None, "empty"),
        )
        for sid, shelter_class in enumerate(shelter_classes if h_pos.has_shelter else [None]):
            for pid, platform_class in enumerate(platform_classes):
                cur_plat = h_pos.platform(platform_class, shelter_class)
                if h_pos.has_shelter:
                    common_notes = (
                        ["noshow"] if shelter_class != "shelter_2" or platform_class != "concrete" else []
                    ) + [shelter_class, platform_class]
                else:
                    common_notes = (["noshow"] if platform_class != "concrete" else []) + [platform_class]
                register(
                    0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x03,
                    0x80,
                    ALayout(
                        corridor_ground, [cur_plat, cur_plat.T] + f2_component, True, notes=common_notes + ["both"]
                    ),
                    cur_sym,
                    internal_category,
                    (f2_name, platform_class, shelter_class, "d"),
                )
                if symmetry.is_symmetrical_y():
                    broken_symmetry = cur_sym.break_y_symmetry()
                    register(
                        0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x01,
                        0x80,
                        ALayout(
                            one_side_ground, [cur_plat, cur_np.T] + f2_component, True, notes=common_notes + ["near"]
                        ),
                        broken_symmetry,
                        internal_category,
                        (f2_name, platform_class, shelter_class, "n"),
                    )
                    named_tiles[(f2_name, platform_class, shelter_class, "f")] = named_tiles[
                        (f2_name, platform_class, shelter_class, "n")
                    ].T
                else:
                    register(
                        0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x01,
                        0x80,
                        ALayout(
                            one_side_ground, [cur_plat, cur_np.T] + f2_component, True, notes=common_notes + ["near"]
                        ),
                        cur_sym,
                        internal_category,
                        (f2_name, platform_class, shelter_class, "n"),
                    )
                    register(
                        0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x02,
                        0x80,
                        ALayout(
                            one_side_ground_t, [cur_np, cur_plat.T] + f2_component, True, notes=common_notes + ["far"]
                        ),
                        cur_sym,
                        internal_category,
                        (f2_name, platform_class, shelter_class, "f"),
                    )
        f2_id += 1


def load(
    f2_id,
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
    window_asym=False,
):
    name = name or source.split("/")[-1]
    v = make_voxel(source)
    f2 = make_f2(v, symmetry)
    f2_window = make_extra(v, symmetry.break_x_symmetry() if window_asym else symmetry, "window")
    f2_window_extender = make_extra(v, symmetry, "window-extender")
    f2_snow = make_extra(v, symmetry, "snow")
    f2_snow_window = make_extra(v, symmetry.break_x_symmetry() if window_asym else symmetry, "snow-window")
    f2_snow_window_extender = make_extra(v, symmetry, "snow-window-extender")

    if window is None:
        window_classes = ["windowed"]
    else:
        window_classes = ["none"] + window

    if "gate" in name or "tiny" in name:
        if window is None:
            f1_snow = make_extra(v, symmetry.break_x_symmetry() if window_asym else symmetry, "snow-window", floor="f1")
        else:
            f1_snow = make_extra(v, symmetry, "snow", floor="f1")
    else:
        f1_snow = None

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

    for window_class in window_classes:
        window_postfix = "" if window_class == "none" else "_" + window_class
        if window is None:
            f2_name = name
        elif window_postfix != "" and name.endswith("_normal"):
            f2_name = name[:-7] + window_postfix
        else:
            f2_name = name + window_postfix
        if window_class == "none":
            f2_component = [f2 + f2_snow]
            cur_sym = symmetry
            cur_bsym = broken_symmetry
        elif window_class == "windowed":
            f2_component = [f2 + f2_window + f2_snow_window]
            if window_asym:
                cur_sym = symmetry.break_x_symmetry()
                cur_bsym = broken_symmetry.break_x_symmetry()
            else:
                cur_sym = symmetry
                cur_bsym = broken_symmetry
        elif window_class == "windowed_extender":
            f2_component = [f2 + f2_window_extender + f2_snow_window_extender]
            cur_sym = symmetry
            cur_bsym = broken_symmetry
        for pid, platform_class in enumerate(platform_classes):
            common_notes = (["noshow"] if platform_class != "concrete" else []) + [platform_class]
            cur_plat = platform_ps[("cns", platform_class, "", "", "")]
            cur_plat_nt = platform_ps[("cns", platform_class, "side", "", "")]
            if corridor:
                register(
                    0x8000 + f2_id * 0x80 + pid * 0x20 + 0x07,
                    0x80,
                    ALayout(
                        corridor_ground,
                        [cur_plat, cur_plat.T, f1 + f1_snow, f1b] + f2_component,
                        True,
                        notes=common_notes + ["third"],
                    ),
                    cur_sym,
                    internal_category,
                    (f2_name, platform_class, None, "corridor"),
                )
            if third:
                register(
                    0x8000 + f2_id * 0x80 + pid * 0x20 + 0x06,
                    0x80,
                    ALayout(
                        one_side_ground,
                        [cur_plat, f1 + f1_snow, h_pos.non_platform.T] + f2_component,
                        True,
                        notes=common_notes + ["third"],
                    ),
                    cur_bsym,
                    internal_category,
                    (f2_name, platform_class, None, "third"),
                )
            for sid, shelter_class in enumerate(shelter_classes if h_pos.has_shelter else [None]):
                if h_pos.has_shelter:
                    common_notes = (
                        ["noshow"] if shelter_class != "shelter_2" or platform_class != "concrete" else []
                    ) + [platform_class, shelter_class]
                else:
                    common_notes = (["noshow"] if platform_class != "concrete" else []) + [platform_class]
                if third:
                    register(
                        0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x05,
                        0x80,
                        ALayout(
                            corridor_ground,
                            [cur_plat_nt, f1 + f1_snow, h_pos.platform(platform_class, shelter_class).T] + f2_component,
                            True,
                            notes=common_notes + ["third", "far"],
                        ),
                        cur_bsym,
                        internal_category,
                        (f2_name, platform_class, shelter_class, "third_f"),
                    )
                if platform:
                    register(
                        0x8000 + f2_id * 0x80 + pid * 0x20 + sid * 0x08 + 0x04,
                        0x80,
                        ALayout(
                            solid_ground,
                            [
                                plat_f1 + f1_snow,
                                h_pos.platform_back_cut(shelter_class).T,
                                concourse_ps[f"{platform_class}"].T,
                            ]
                            + f2_component,
                            False,
                            notes=common_notes + ["far"],
                        ),
                        cur_bsym,
                        internal_category,
                        (f2_name, platform_class, shelter_class, "platform"),
                    )
        if full:
            register(
                0xFB00 + f2_id,
                1,
                ALayout(solid_ground, [full_f1 + f1_snow, concourse] + f2_component, False),
                cur_sym,
                internal_category,
                (f2_name, None, None, ""),
            )
        f2_id += 1


def load_full(f2_id, source, symmetry, internal_category, name=None, h_pos=Normal, borrow_f1=None, window=None):
    load(
        f2_id,
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
named_tiles = AttrDict(schema=("name", "platform_class", "shelter_class", "f1_layout"))

load(0x00, "front_normal", BuildingSpriteSheetSymmetricalX, "F0", corridor=False, window=[])
load(0x01, "front_gate", BuildingSpriteSheetFull, "F0", corridor=False)
load(0x03, "front_gate_extender", BuildingSpriteSheetSymmetricalX, "F0", corridor=False)

load(0x04, "corner", BuildingSpriteSheetFull, "F1", h_pos=SideNarrow, corridor=False, window=[])
load(0x08, "corner_gate", BuildingSpriteSheetFull, "F1", h_pos=SideNarrow, corridor=False)
load(0x12, "corner_2", BuildingSpriteSheetFull, "F1", h_pos=SideNarrow, corridor=False, window=[])
load(0x16, "corner_gate_2", BuildingSpriteSheetFull, "F1", h_pos=SideNarrow, corridor=False)

load_central(
    0x20, "central", BuildingSpriteSheetSymmetrical, "N", window=["windowed", "windowed_extender"], window_asym=True
)

load_central(0x23, "side_a", BuildingSpriteSheetFull, "A", h_pos=Side, window=["windowed"])
load_central(0x2B, "side_a2", BuildingSpriteSheetSymmetricalY, "A", h_pos=Side, window=["windowed"])
load_central(0x2F, "side_a3", BuildingSpriteSheetFull, "A", h_pos=Side, window=["windowed"])
load_central(0x37, "side_b", BuildingSpriteSheetFull, "B", h_pos=Side, window=[])
load_central(0x3B, "side_b2", BuildingSpriteSheetSymmetricalY, "B", h_pos=Side, window=[])
load_central(0x3D, "side_c", BuildingSpriteSheetSymmetricalY, "C", h_pos=Side, window=[])
load_central(0x3F, "side_d", BuildingSpriteSheetSymmetricalY, "D", h_pos=Side)

load(0x41, "h_end", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False, window=[])
load_full(0x43, "h_end_untraversable", BuildingSpriteSheetSymmetricalY, "H", window=[])
load(0x45, "h_end_asym", BuildingSpriteSheetFull, "H", h_pos=SideNarrow, corridor=False, window=[])
load(0x49, "h_end_asym_gate", BuildingSpriteSheetFull, "H", h_pos=SideNarrow, corridor=False)
load(0x4D, "h_end_gate", BuildingSpriteSheetSymmetricalY, "H", full=False, platform=False, third=False)
load_full(0x4F, "h_end_gate_untraversable", BuildingSpriteSheetSymmetricalY, "H")
load(0x51, "h_normal", BuildingSpriteSheetSymmetrical, "H", window=[])
load(0x52, "h_gate", BuildingSpriteSheetSymmetricalY, "H", third=False, platform=False)
load(0x54, "h_gate_1", BuildingSpriteSheetFull, "H", asym=True)
load(0x58, "h_gate_extender", BuildingSpriteSheetSymmetrical, "H", third=False, platform=False)
load(0x59, "h_gate_extender_1", BuildingSpriteSheetSymmetricalX, "H", asym=True)

load(0x5B, "v_end", BuildingSpriteSheetSymmetricalX, "F0", h_pos=VNarrow, corridor=False)
load(0x5D, "v_end_gate", BuildingSpriteSheetSymmetricalX, "F0", h_pos=VNarrow, corridor=False)
load_central(0x5F, "v_central", BuildingSpriteSheetSymmetrical, "N", h_pos=V)

load(0x60, "tiny", BuildingSpriteSheetSymmetrical, "H", h_pos=V, full=False, platform=False, third=False)
load_full(0x61, "tiny_untraversable", BuildingSpriteSheetSymmetrical, "H")
load(0x62, "tiny_asym", BuildingSpriteSheetSymmetricalX, "H", h_pos=TinyAsym, corridor=False)

load_full(0x80, "irregular/turn", BuildingSpriteSheetFull, "T")
load_full(0x84, "irregular/turn_gate", BuildingSpriteSheetFull, "T")
load(0x88, "irregular/tee", BuildingSpriteSheetSymmetricalX, "T", corridor=False, borrow_f1="h_normal")
load(0x8A, "irregular/cross", BuildingSpriteSheetSymmetrical, "T", platform=False, full=False, borrow_f1="h_normal")
load_full(0x8B, "irregular/double_corner", BuildingSpriteSheetRotational, "T", borrow_f1="h_normal", window=[])
load(0x8F, "irregular/funnel", BuildingSpriteSheetFull, "T", corridor=False, borrow_f1="h_normal", window=[])
load_full(0x93, "irregular/inner_corner", BuildingSpriteSheetFull, "T", window=[])
load_full(0x97, "irregular/double_inner_corner", BuildingSpriteSheetSymmetricalY, "T", borrow_f1="h_normal")
load_full(0x99, "irregular/v_funnel", BuildingSpriteSheetFull, "T")
load_full(0x9D, "irregular/v_funnel_2", BuildingSpriteSheetFull, "T")

load_full(0xC0, "junction/front_corner", BuildingSpriteSheetDiagonal, "X", window=[])
load_full(0xC4, "junction/front_gate_extender_corner", BuildingSpriteSheetDiagonal, "X")
load_full(0xC8, "junction/double_corner_2", BuildingSpriteSheetDiagonal, "X", window=[])
load_full(0xCC, "junction/bicorner", BuildingSpriteSheetDiagonal, "X", window=[])
load_full(0xD0, "junction/bicorner_2", BuildingSpriteSheetDiagonal, "X", window=[])

named_tiles.populate()


def globalize_all(platform_class=None, shelter_class=None):

    caller_globals = inspect.currentframe().f_back.f_globals

    platform_tiles.globalize(caller_globals=caller_globals, platform_class=platform_class, shelter_class=shelter_class)
    two_side_tiles.globalize(
        caller_globals=caller_globals,
        platform_class=platform_class,
        shelter_class=shelter_class,
        platform_class_2=platform_class,
        shelter_class_2=shelter_class,
    )
    concourse_tiles.globalize(caller_globals=caller_globals, platform_class=platform_class, shelter_class=shelter_class)
    named_tiles.globalize(caller_globals=caller_globals, platform_class=platform_class, shelter_class=shelter_class)
