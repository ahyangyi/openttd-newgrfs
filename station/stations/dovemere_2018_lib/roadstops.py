import grf
from station.lib import (
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetricalX,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.graphics import SCALE_TO_ZOOM
from agrf.magic import Switch
from datetime import date
from roadstop.lib import ARoadStop
from station.lib import ALayout
from ..misc import road_ground

roadstops = []
WIDTH = 3
OVERPASS_HEIGHT = 10
OVERHANG_WIDTH = 1


for name, sym, (far, overhang, overpass, near) in [
    ("overpass", BuildingSpriteSheetSymmetricalX, (True, True, True, False)),
    ("west_stair", BuildingSpriteSheetFull, (True, False, True, True)),
    ("west_stair_extender", BuildingSpriteSheetSymmetricalX, (True, True, True, True)),
]:
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    farv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_back_mask.vox", "back")
    farv.in_place_subset(sym.render_indices())
    farsprite = sym.create_variants(farv.spritesheet(xspan=WIDTH))
    farps = AParentSprite(farsprite, (16, WIDTH, 12), (0, 0, 0))

    overpassv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_overpass_mask.vox", "overpass")
    overpassv.in_place_subset(sym.render_indices())
    if overhang:
        overpasssprite = sym.create_variants(
            overpassv.spritesheet(xspan=OVERHANG_WIDTH, xdiff=WIDTH, zdiff=OVERPASS_HEIGHT * 2)
        )
        overpassps = AParentSprite(
            overpasssprite, (16, OVERHANG_WIDTH, 12 - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)
        )
    else:
        overpasssprite = sym.create_variants(
            overpassv.spritesheet(xspan=16 - WIDTH * 2, xdiff=WIDTH, zdiff=OVERPASS_HEIGHT * 2)
        )
        overpassps = AParentSprite(
            overpasssprite, (16, 16 - WIDTH * 2, 12 - OVERPASS_HEIGHT), (0, WIDTH, OVERPASS_HEIGHT)
        )

    nearv = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_front_mask.vox", "front")
    nearv.in_place_subset(sym.render_indices())
    nearsprite = sym.create_variants(nearv.spritesheet(xspan=WIDTH, xdiff=16 - WIDTH))
    nearps = AParentSprite(nearsprite, (16, WIDTH, 12), (0, 16 - WIDTH, 0))

    layout = ALayout(
        road_ground,
        [farps] + ([overpassps] if overpass else []) + ([nearps] if near else []),
        True,
        category=b"\xe8\x8a\x9cR",
    )

    for cur in [layout, layout.R, layout.T, layout.T.R] if (sym is BuildingSpriteSheetFull) else [layout, layout.T]:
        cur_roadstop = ARoadStop(
            id=len(roadstops),
            translation_name="STRAIGHT_STAIR",
            graphics=Switch(ranges={4: cur, 5: cur.M}, default=cur, code="view"),
            general_flags=0x8,
            class_label=b"\xe8\x8a\x9cR",
            doc_layout=cur,
        )
        roadstops.append(cur_roadstop)