import grf
from station.lib import BuildingSpriteSheetFull, AGroundSprite, AParentSprite, ALayout
from agrf.graphics.voxel import LazyVoxel
from datetime import date
from grfobject.lib import AObject
from station.lib import ALayout
from .layouts import solid_ground

v = LazyVoxel(
    "west_stair",
    prefix="station/voxels/render/dovemere_2018/plaza",
    voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/west_stair.vox": path,
    load_from="station/files/cns-gorender.json",
    # config={"z_scale": 1.01},
)
sprite = BuildingSpriteSheetFull.create_variants(v.spritesheet())
ps = AParentSprite(sprite, (16, 16, 12), (0, 0, 0))
test_layout = ALayout(solid_ground, [ps], True)
test_object = AObject(
    id=0x0,
    translation_name="STRAIGHT_STAIR",
    layouts=[test_layout, test_layout.R, test_layout.T, test_layout.T.R],
    class_label=b"\xe8\x8a\x9cZ",
    climates_available=grf.ALL_CLIMATES,
    size=(1, 1),
    num_views=4,
    introduction_date=date(1900, 1, 1),
    end_of_life_date=date(2025, 1, 1),
    height=1,
    flags=grf.Object.Flags.ONLY_IN_GAME,
)
