from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    AParentSprite,
    ALayout,
    AChildSprite,
    AttrDict,
    Registers,
)
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from roadstop.lib import ARoadStop
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from ..misc import road_ground

named_parts = AttrDict(schema=("name", "part"))
named_layouts = AttrDict(schema=("name",))

cnt = 0
roadstops = []
WIDTH = 3
TOTAL_HEIGHT = 12
OVERPASS_HEIGHT = 11
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 9

JOGGLE_AMOUNT = 45 - 32 * 2**0.5


def register_road_stop(layout, sym):
    global cnt
    for cur in sym.get_all_variants(layout)[::2]:
        cur_roadstop = ARoadStop(
            id=0x8000 + cnt,
            translation_name="WEST_PLAZA_BUS",
            graphics=Switch(ranges={4: cur, 5: cur.M}, default=cur, code="view"),
            general_flags=0x8,
            class_label=b"\xe8\x8a\x9cR",
            enable_if=[parameter_list["E88A9CA_ENABLE_ROADSTOP"]],
            doc_layout=cur,
        )
        roadstops.append(cur_roadstop)
        cur_roadstop = ARoadStop(
            id=0xC000 + cnt,
            translation_name="WEST_PLAZA_BUS",
            graphics=Switch(ranges={4: cur, 5: cur.M}, default=cur, code="view"),
            general_flags=0x8,
            class_label=b"\xe8\x8a\x9cR",
            enable_if=[parameter_list["E88A9CA_ENABLE_ROADSTOP"]],
            doc_layout=cur,
            is_waypoint=True,
        )
        roadstops.append(cur_roadstop)
        cnt += 1


def make_road_stop(name, sym, far, overpass, near, extended, floating, joggle=0):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    # For better handling of pillars/bollards
    v.config["tiling_mode"] = "reflect"
    v.config["joggle"] = joggle
    if extended:
        v.config["size"]["x"] = 448
        v.config["size"]["y"] = 448
        for sprite in v.config["sprites"]:
            sprite["width"] = 112
        v.config["agrf_zdiff"] = -12

    snow = v.keep_layers(("snow",), "snow")
    snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    snow.config["agrf_childsprite"] = (0, -3)

    nosnow = v.discard_layers(("snow",), "nosnow")
    nosnow.config["agrf_manual_crop"] = (0, 3)

    extended_suffix = "_extended" if extended else ""

    ps = []
    for part, partname in ((far, "far"), (overpass, "overpass"), (near, "near")):
        if part is None:
            continue
        span, offset = part

        def make_part(v):
            partv = v.mask_clip_away(
                f"station/voxels/dovemere_2018/masks/road_{partname}_mask{extended_suffix}.vox", partname
            )
            partv.in_place_subset(sym.render_indices())
            partsprite = sym.create_variants(
                partv.spritesheet(
                    xspan=span[1], yspan=span[0], xdiff=offset[1], ydiff=offset[0], zdiff=offset[2] + floating
                )
            )
            return partsprite

        partps = AParentSprite(make_part(nosnow), span, offset)
        partsnow = make_part(snow)
        partsnow.voxel.render()
        snowcs = AChildSprite(partsnow, (0, 0), flags={"dodraw": Registers.SNOW})
        partps = partps + snowcs
        named_parts[(name, partname)] = partps
        ps.append(partps)

    layout = ALayout(road_ground, ps, True, category=b"\xe8\x8a\x9cR")
    named_layouts[(name,)] = layout

    register_road_stop(layout, sym)


make_road_stop(
    "overpass",
    BuildingSymmetricalX,
    ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
    ((16, OVERHANG_WIDTH, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
    None,
    False,
    0,
    joggle=JOGGLE_AMOUNT,
)


overpass_far = named_parts[("overpass", "far")]
overpass_overpass = named_parts[("overpass", "overpass")]
layout = ALayout(
    road_ground, [overpass_far, overpass_overpass, overpass_far.T, overpass_overpass.T], True, category=b"\xe8\x8a\x9cR"
)
named_layouts[("double_overpass",)] = layout
register_road_stop(layout, BuildingSymmetrical)
