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
ROAD_STOP_WIDTH = 3


for name, sym, (far, overpass, near) in [
    ("overpass", BuildingSpriteSheetSymmetricalX, (True, False, False)),
    ("west_stair", BuildingSpriteSheetFull, (True, True, True)),
    ("west_stair_extender", BuildingSpriteSheetSymmetricalX, (True, True, True)),
]:
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    far = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_back_mask.vox", "back")
    far.in_place_subset(sym.render_indices())
    farsprite = sym.create_variants(far.spritesheet(xspan=ROAD_STOP_WIDTH))
    farps = AParentSprite(farsprite, (16, ROAD_STOP_WIDTH, 12), (0, 0, 0))

    near = v.mask_clip_away("station/voxels/dovemere_2018/masks/road_front_mask.vox", "front")
    near.in_place_subset(sym.render_indices())
    nearsprite = sym.create_variants(near.spritesheet(xspan=ROAD_STOP_WIDTH, xdiff=16 - ROAD_STOP_WIDTH))
    nearps = AParentSprite(nearsprite, (16, ROAD_STOP_WIDTH, 12), (0, 16 - ROAD_STOP_WIDTH, 0))

    layout = ALayout(road_ground, [farps] + ([nearps] if near else []), True, category=b"\xe8\x8a\x9cR")

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
