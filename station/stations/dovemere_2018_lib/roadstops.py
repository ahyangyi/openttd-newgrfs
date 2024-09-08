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
from .layouts import solid_ground

roadstop_doc_layouts = []
roadstops = []

img_1 = grf.ImageFile("third_party/opengfx2/road1.png")
sprite_1 = grf.AlternativeSprites(
    grf.FileSprite(img_1, 0, 0, 256, 127, xofs=-124, yofs=0, zoom=SCALE_TO_ZOOM[4], bpp=32, crop=False)
)
img_2 = grf.ImageFile("third_party/opengfx2/road2.png")
sprite_2 = grf.AlternativeSprites(
    grf.FileSprite(img_2, 0, 0, 256, 127, xofs=-124, yofs=0, zoom=SCALE_TO_ZOOM[4], bpp=32, crop=False)
)
sprite = BuildingSpriteSheetSymmetrical.create_variants([sprite_1, sprite_2])
cs = AChildSprite(sprite, (0, 0))


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
    layout = ALayout(solid_ground + cs, [ps], True, category=b"\xe8\x8a\x9cZ")

    for cur in [layout, layout.R] if (sym is BuildingSpriteSheetFull) else [layout]:
        cur_roadstop = ARoadStop(
            id=len(roadstops),
            translation_name="STRAIGHT_STAIR",
            layouts=[cur, cur.R.M, cur.T.R, cur.T.M],
            class_label=b"\xe8\x8a\x9cZ",
        )
        # FIXME doesn't need thiz
        cur.station_id = 0xE000 + len(roadstops)
        roadstop_doc_layouts.append(cur)
        roadstops.append(cur_roadstop)
