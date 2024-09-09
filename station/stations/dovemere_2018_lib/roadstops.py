import grf
from station.lib import (
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetrical,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.graphics import SCALE_TO_ZOOM
from datetime import date
from roadstop.lib import ARoadStop
from station.lib import ALayout
from ..misc import road_ground

roadstop_doc_layouts = []
roadstops = []


for name, sym in [("overpass", BuildingSpriteSheetSymmetricalX), ("west_stair", BuildingSpriteSheetFull)]:
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    sprite = sym.create_variants(v.spritesheet())
    ps = AParentSprite(sprite, (16, 16, 12), (0, 0, 0))
    layout = ALayout(road_ground, [ps], True, category=b"\xe8\x8a\x9cR")

    for cur in [layout, layout.R] if (sym is BuildingSpriteSheetFull) else [layout]:
        cur_roadstop = ARoadStop(
            id=len(roadstops),
            translation_name="STRAIGHT_STAIR",
            layouts=[cur, cur.R.M, cur.T.R, cur.T.M],
            class_label=b"\xe8\x8a\x9cR",
        )
        # FIXME doesn't need thiz
        cur.station_id = 0xF000 + len(roadstops)
        roadstop_doc_layouts.append(cur)
        roadstops.append(cur_roadstop)
