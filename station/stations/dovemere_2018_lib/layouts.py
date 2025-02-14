import os
import inspect
import types
from station.lib import (
    BuildingFull,
    BuildingSymmetrical,
    BuildingSymmetricalX,
    BuildingSymmetricalY,
    BuildingRotational,
    BuildingDiagonal,
    BuildingCylindrical,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
    Registers,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.sprites import empty_alternatives
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
from station.stations.ground import named_ps as ground_ps, named_tiles as ground_tiles
from station.stations.misc import track_ground, track
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from dataclasses import dataclass


base_height = 14
building_height = 48
overpass_height = building_height - base_height

gray_layout = ground_tiles.gray
gray_ps = ground_ps.gray
concourse = concourse_ps.none

# FIXME: technically should be 21 instead of 20, but in reality that results in bad effects
JOGGLE_AMOUNT = (16 * 2**0.5 - 20) / 1.25


def make_empty_variant(w, h, x, y, offset=0, span=16):
    if offset == 0 and span == 16:
        empty_image = empty_alternatives(w, h, x, y)
        empty_image.squash = types.MethodType(lambda self, *args, empty_image=empty_image: self, empty_image)
        return BuildingCylindrical.create_variants([empty_image])
    deltas = [[-2, -1], [2, -1], [-2, -1], [2, -1], [2, 1], [-2, 1], [2, 1], [-2, 1]]
    offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [-2, -1], [2, -1], [-2, -1], [2, -1]]

    empty_images = []
    for i in range(8):
        x1 = x + deltas[i][0] * offset + offsets[i][0] * (16 - span)
        y1 = y + deltas[i][1] * offset + offsets[i][1] * (16 - span)

        empty_image = empty_alternatives(w, h, x1, y1)
        empty_image.squash = types.MethodType(lambda self, *args, empty_image=empty_image: self, empty_image)
        empty_images.append(empty_image)
    return BuildingFull.create_variants(empty_images)


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


snow_layers = tuple(y for x in ("snow", "snow-window", "snow-window-extender") for y in (x, x + "-boundary"))
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

f1_empty_offset = (-31, -14)
f1_empty_sprite = {}
for k, (_, offset, span) in f1_subsets.items():
    f1_empty_sprite[k] = make_empty_variant(64, 48, *f1_empty_offset, offset, span)
f2_empty_offset = (-31, -34)
f2_empty_sprite = make_empty_variant(64, 68, *f2_empty_offset)


def make_f2(v, sym):
    v = v.discard_layers(all_f1_layers + all_f2_layers + snow_layers, "f2")
    v.in_place_subset(sym.render_indices())
    v.config["agrf_relative_childsprite"] = f2_empty_offset
    s = sym.create_variants(v.spritesheet(zdiff=base_height))

    empty_parent = AParentSprite(f2_empty_sprite, (16, 16, overpass_height), (0, 0, base_height + platform_height))
    f2_child = AChildSprite(s, (0, 0), palette=0, flags={"add_palette": Registers.RECOLOUR_OFFSET})

    return empty_parent + f2_child


def make_extra(v, sym, name, floor="f2"):
    vd = v.keep_layers((name, name + "-boundary"), name)
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
        v.config["agrf_relative_childsprite"] = f2_empty_offset
        zdiff = base_height
    else:
        v.config["agrf_relative_childsprite"] = f1_empty_offset
        zdiff = 0
    v.in_place_subset(sym.render_indices())
    s = sym.create_variants(v.spritesheet(zdiff=zdiff))
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
        V.config["agrf_relative_childsprite"] = f1_empty_offset
        s = sym.create_variants(V.spritesheet())
        empty_parent = AParentSprite(f1_empty_sprite[subset], (16, xspan, base_height), (0, xdiff, platform_height))
        f1_child = AChildSprite(s, (0, 0))
        f1_cache[(v, subset)] = empty_parent + f1_child, sym
    ret, ret_sym = f1_cache[(v, subset)]
    assert sym is ret_sym
    return ret


def register(base_id, step_id, l, symmetry, internal_category, name, broken_near_hack=False):
    l = symmetry.get_all_variants(l)
    cnt = len(l)
    for i, layout in enumerate(l):
        layout.category = get_category(internal_category, i >= cnt // 2, layout.notes, layout.traversable)
    layouts.extend(l)
    l = symmetry.create_variants(l)
    cur_entries = symmetry.get_all_entries(l)
    cnt = len(cur_entries)
    for i, entry in enumerate(cur_entries):
        if broken_near_hack:
            entry.id = base_id + step_id * (i % (cnt // 2)) + (i // (cnt // 2))
        else:
            entry.id = base_id + step_id * i
        entries.append(entry)
    named_tiles[name] = l


solid_ground = gray_ps
# FIME merge these since the groundchildsprite is no longer used here
corridor_ground = track_ground
one_side_ground = track_ground
one_side_ground_t = track_ground
empty_ground = track_ground

voxel_cache = {}


def make_voxel(source):
    if source not in voxel_cache:
        voxel_cache[source] = LazyVoxel(
            os.path.basename(source),
            prefix=os.path.join(".cache/render/station/dovemere_2018", os.path.dirname(source)),
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/{source}.vox": path,
            load_from="station/files/gorender.json",
        )
        voxel_cache[source].config["joggle"] = JOGGLE_AMOUNT
    return voxel_cache[source]


def load_central(f2_ids, source, symmetry, internal_category, name=None, h_pos=Normal, window=None, window_asym=False):
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

    if isinstance(f2_ids, int):
        f2_ids = (f2_ids,)

    for window_class, f2_id in zip(window_classes, f2_ids):
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
                        broken_near_hack=True,
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
    borrow_f1_symmetry=BuildingSymmetrical,
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

load(0x00, "front_normal", BuildingSymmetricalX, "F0", corridor=False, window=[])
load(0x02, "front_gate", BuildingFull, "F0", corridor=False)
load(0x06, "front_gate_extender", BuildingSymmetricalX, "F0", corridor=False)

load(0x08, "corner", BuildingFull, "F1", h_pos=SideNarrow, corridor=False, window=[])
load(0x0C, "corner_gate", BuildingFull, "F1", h_pos=SideNarrow, corridor=False)
load(0x10, "corner_2", BuildingFull, "F1", h_pos=SideNarrow, corridor=False, window=[])
load(0x14, "corner_gate_2", BuildingFull, "F1", h_pos=SideNarrow, corridor=False)

load_central(
    (0x20, 0x21, 0x23), "central", BuildingSymmetrical, "N", window=["windowed", "windowed_extender"], window_asym=True
)

load_central((0x24, 0x28), "side_a", BuildingFull, "A", h_pos=Side, window=["windowed"])
load_central((0x2C, 0x2E), "side_a2", BuildingSymmetricalY, "A", h_pos=Side, window=["windowed"])
load_central((0x30, 0x34), "side_a3", BuildingFull, "A", h_pos=Side, window=["windowed"])
load_central(0x38, "side_b", BuildingFull, "B", h_pos=Side, window=[])
load_central(0x3C, "side_b2", BuildingSymmetricalY, "B", h_pos=Side, window=[])
load_central(0x3E, "side_c", BuildingSymmetricalY, "C", h_pos=Side, window=[])
load_central(0x40, "side_d", BuildingSymmetricalY, "D", h_pos=Side)

load(0x42, "h_end", BuildingSymmetricalY, "H", full=False, platform=False, window=[])
load_full(0x44, "h_end_untraversable", BuildingSymmetricalY, "H", window=[])
load(0x46, "h_end_asym", BuildingFull, "H", h_pos=SideNarrow, corridor=False, window=[])
load(0x4A, "h_end_asym_gate", BuildingFull, "H", h_pos=SideNarrow, corridor=False)
load(0x4E, "h_end_gate", BuildingSymmetricalY, "H", full=False, platform=False, third=False)
load_full(0x50, "h_end_gate_untraversable", BuildingSymmetricalY, "H")
load(0x52, "h_normal", BuildingSymmetrical, "H", window=[])
load(0x53, "h_gate", BuildingSymmetricalY, "H", third=False, platform=False)
load(0x55, "h_gate_1", BuildingFull, "H", asym=True)
load(0x59, "h_gate_extender", BuildingSymmetrical, "H", third=False, platform=False)
load(0x5A, "h_gate_extender_1", BuildingSymmetricalX, "H", asym=True)

load(0x5C, "v_end", BuildingSymmetricalX, "F0", h_pos=VNarrow, corridor=False)
load(0x5E, "v_end_gate", BuildingSymmetricalX, "F0", h_pos=VNarrow, corridor=False)
load_central(0x60, "v_central", BuildingSymmetrical, "N", h_pos=V)

load(0x61, "tiny", BuildingSymmetrical, "H", h_pos=V, full=False, platform=False, third=False)
load_full(0x62, "tiny_untraversable", BuildingSymmetrical, "H")
load(0x63, "tiny_asym", BuildingSymmetricalX, "H", h_pos=TinyAsym, corridor=False)

load_full(0x80, "irregular/turn", BuildingFull, "T")
load_full(0x84, "irregular/turn_gate", BuildingFull, "T")
load(0x88, "irregular/tee", BuildingSymmetricalX, "T", corridor=False, borrow_f1="h_normal")
load(0x8A, "irregular/cross", BuildingSymmetrical, "T", platform=False, full=False, borrow_f1="h_normal")
load_full(0x8B, "irregular/double_corner", BuildingRotational, "T", borrow_f1="h_normal", window=[])
load(0x8F, "irregular/funnel", BuildingFull, "T", corridor=False, borrow_f1="h_normal", window=[])
load_full(0x93, "irregular/inner_corner", BuildingFull, "T", window=[])
load_full(0x97, "irregular/double_inner_corner", BuildingSymmetricalY, "T", borrow_f1="h_normal")
load_full(0x99, "irregular/v_funnel", BuildingFull, "T")
load_full(0x9D, "irregular/v_funnel_2", BuildingFull, "T")

load_full(0xC0, "junction/front_corner", BuildingDiagonal, "X", window=[])
load_full(0xC4, "junction/front_gate_extender_corner", BuildingDiagonal, "X")
load_full(0xC8, "junction/double_corner_2", BuildingDiagonal, "X", window=[])
load_full(0xCC, "junction/bicorner", BuildingDiagonal, "X", window=[])
load_full(0xD0, "junction/bicorner_2", BuildingDiagonal, "X", window=[])

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
    caller_globals["concourse_none"] = concourse_tiles.none
