import grf
from station.lib import BuildingSpriteSheetFull, BuildingSpriteSheetSymmetricalX, AGroundSprite, AParentSprite, ALayout
from agrf.graphics.voxel import LazyVoxel
from datetime import date
from grfobject.lib import AObject
from station.lib import ALayout
from .layouts import solid_ground

objects = []

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
    layout = ALayout(solid_ground, [ps], True)

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
        )
        objects.append(cur_object)
