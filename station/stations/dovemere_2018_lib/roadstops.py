from station.lib import BuildingFull, BuildingSymmetricalX, AParentSprite, ALayout, AttrDict
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from roadstop.lib import ARoadStop
from ..misc import road_ground

named_layouts = AttrDict(schema=("name",))

cnt = 0
roadstops = []
WIDTH = 3
TOTAL_HEIGHT = 12
OVERPASS_HEIGHT = 10
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 9


def make_road_stop(name, sym, far, overpass, near, extended, floating):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    if extended:
        v.config["size"]["x"] = 448
        v.config["size"]["y"] = 448
        for sprite in v.config["sprites"]:
            sprite["width"] = 112
        v.config["agrf_zdiff"] = -12
    extended_suffix = "_extended" if extended else ""

    ps = []
    for part, partname in ((far, "far"), (overpass, "overpass"), (near, "near")):
        if part is None:
            continue
        span, offset = part
        partv = v.mask_clip_away(
            f"station/voxels/dovemere_2018/masks/road_{partname}_mask{extended_suffix}.vox", partname
        )
        partv.in_place_subset(sym.render_indices())
        partsprite = sym.create_variants(
            partv.spritesheet(
                xspan=span[1], yspan=span[0], xdiff=offset[1], ydiff=offset[0], zdiff=offset[2] + floating
            )
        )
        partps = AParentSprite(partsprite, span, offset)
        ps.append(partps)

    layout = ALayout(road_ground, ps, True, category=b"\xe8\x8a\x9cR")
    named_layouts[(name,)] = layout

    global cnt
    for cur in [layout, layout.R, layout.T, layout.T.R] if (sym is BuildingFull) else [layout, layout.T]:
        cur_roadstop = ARoadStop(
            id=0x8000 + cnt,
            translation_name="WEST_PLAZA_BUS",
            graphics=Switch(ranges={4: cur, 5: cur.M}, default=cur, code="view"),
            general_flags=0x8,
            class_label=b"\xe8\x8a\x9cR",
            enable_if=[parameter_list.index("E88A9CA_ENABLE_ROADSTOP")],
            doc_layout=cur,
        )
        roadstops.append(cur_roadstop)
        cur_roadstop = ARoadStop(
            id=0xC000 + cnt,
            translation_name="WEST_PLAZA_BUS",
            graphics=Switch(ranges={4: cur, 5: cur.M}, default=cur, code="view"),
            general_flags=0x8,
            class_label=b"\xe8\x8a\x9cR",
            enable_if=[parameter_list.index("E88A9CA_ENABLE_ROADSTOP")],
            doc_layout=cur,
            is_waypoint=True,
        )
        roadstops.append(cur_roadstop)
        cnt += 1


make_road_stop(
    "overpass",
    BuildingSymmetricalX,
    ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
    ((16, OVERHANG_WIDTH, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
    None,
    False,
    0,
)
make_road_stop(
    "west_stair",
    BuildingFull,
    ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
    ((16, 16 - WIDTH * 2, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
    ((16, EXTENDED_WIDTH, TOTAL_HEIGHT), (0, 16 - WIDTH, 0)),
    True,
    16,
)
make_road_stop(
    "west_stair_extender",
    BuildingSymmetricalX,
    ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
    ((16, 16 - WIDTH * 2, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
    ((16, EXTENDED_WIDTH, TOTAL_HEIGHT), (0, 16 - WIDTH, 0)),
    True,
    0,
)
make_road_stop(
    "west_stair_end",
    BuildingFull,
    ((16, WIDTH, TOTAL_HEIGHT), (0, 0, 0)),
    ((16, 16 - WIDTH * 2, TOTAL_HEIGHT - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)),
    ((16, EXTENDED_WIDTH, TOTAL_HEIGHT), (0, 16 - WIDTH, 0)),
    True,
    16,
)
