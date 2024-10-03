from station.lib import BuildingFull, BuildingSymmetricalX, AParentSprite, ALayout
from station.lib.parameters import parameter_list
from agrf.graphics.voxel import LazyVoxel
from agrf.magic import Switch
from roadstop.lib import ARoadStop
from ..misc import road_ground

cnt = 0
roadstops = []
WIDTH = 3
OVERPASS_HEIGHT = 10
OVERHANG_WIDTH = 1
EXTENDED_WIDTH = 8


for name, sym, (far, overhang, overpass, near), extended in [
    ("overpass", BuildingSymmetricalX, (True, True, True, False), False),
    ("west_stair", BuildingFull, (True, False, True, True), True),
    ("west_stair_extender", BuildingSymmetricalX, (True, False, True, True), True),
]:
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    if extended:
        v.config["size"]["x"] = 384
        v.config["size"]["y"] = 384
        for sprite in v.config["sprites"]:
            sprite["width"] = 96
        v.config["agrf_zdiff"] = -8
    if extended:
        farv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_back_mask_extended.vox", "back")
    else:
        farv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_back_mask.vox", "back")
    farv.in_place_subset(sym.render_indices())
    farsprite = sym.create_variants(farv.spritesheet(xspan=WIDTH))
    farps = AParentSprite(farsprite, (16, WIDTH, 12), (0, 0, 0))

    if extended:
        overpassv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_overpass_mask_extended.vox", "overpass")
    else:
        overpassv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_overpass_mask.vox", "overpass")
    overpassv.in_place_subset(sym.render_indices())
    if overhang:
        overpasssprite = sym.create_variants(
            overpassv.spritesheet(xspan=OVERHANG_WIDTH, xdiff=WIDTH, zdiff=OVERPASS_HEIGHT)
        )
        overpassps = AParentSprite(
            overpasssprite, (16, OVERHANG_WIDTH, 12 - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)
        )
    else:
        overpasssprite = sym.create_variants(
            overpassv.spritesheet(xspan=16 - WIDTH * 2, xdiff=WIDTH, zdiff=OVERPASS_HEIGHT)
        )
        overpassps = AParentSprite(
            overpasssprite, (16, 16 - WIDTH * 2, 12 - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)
        )

    if extended:
        nearv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_front_mask_extended.vox", "front")
    else:
        nearv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_front_mask.vox", "front")
    nearv.in_place_subset(sym.render_indices())
    nearsprite = sym.create_variants(nearv.spritesheet(xspan=WIDTH, xdiff=16 - WIDTH))
    if extended:
        nearps = AParentSprite(nearsprite, (16, EXTENDED_WIDTH, 12), (0, 16 - WIDTH, 0))
    else:
        nearps = AParentSprite(nearsprite, (16, WIDTH, 12), (0, 16 - WIDTH, 0))

    layout = ALayout(
        road_ground,
        [farps] + ([overpassps] if overpass else []) + ([nearps] if near else []),
        True,
        category=b"\xe8\x8a\x9cR",
    )

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
