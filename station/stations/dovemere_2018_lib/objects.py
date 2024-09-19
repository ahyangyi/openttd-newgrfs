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
from grfobject.lib import AObject
from station.lib import ALayout
from .layouts import solid_ground

objects = []

for name, sym in [("west_plaza_center", BuildingSpriteSheetSymmetrical)]:
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(v.spritesheet())
    # ps = AParentSprite(sprite, (16, 16, 12), (0, 0, 0))
    # layout = ALayout(solid_ground + cs, [ps], True, category=b"\xe8\x8a\x9cZ")
    gs = AGroundSprite(sprite)
    layout = ALayout(gs, [], True, category=b"\xe8\x8a\x9cZ")

    for cur in [layout, layout.R] if (sym is BuildingSpriteSheetFull) else [layout]:
        cur_object = AObject(
            id=len(objects),
            translation_name="STRAIGHT_STAIR",
            layouts=[cur, cur.R.M, cur.T.R, cur.T.M],
            class_label=b"\xe8\x8a\x9cZ",
            climates_available=grf.ALL_CLIMATES,
            size=(1, 1),
            num_views=4,
            introduction_date=0,
            end_of_life_date=0,
            height=1,
            flags=grf.Object.Flags.ONLY_IN_GAME,
            doc_layout=cur,
        )
        objects.append(cur_object)
