from bridge.lib import ABridge
import grf

from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet

vox = LazyVoxel(
    "dovemere_yangtze_1",
    prefix=".cache/render/bridge/dovemere_yangtze_1",
    voxel_getter=lambda: "bridge/voxels/dovemere_yangtze_1.vox",
    load_from="bridge/files/gorender.json",
)
voxels = [LazySpriteSheet([vox], [(0, 0)])]

the_bridge = ABridge(
    id=0x01,
    translation_name="YANGTZE_I",
    intro_year_since_1920=0,
    min_length=4,
    max_length=32,
    layout={
        "table_id": 0,
        "tables": [
            [
                grf.SpriteRef(0x09BD, is_global=True),
                grf.SpriteRef(0x09C1, is_global=True),
                grf.SpriteRef(0x09C9, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x09BE, is_global=True),
                grf.SpriteRef(0x09C2, is_global=True),
                grf.SpriteRef(0x09CA, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x09BF, is_global=True),
                grf.SpriteRef(0x09C1, is_global=True),
                grf.SpriteRef(0x09C9, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x09C0, is_global=True),
                grf.SpriteRef(0x09C2, is_global=True),
                grf.SpriteRef(0x09CA, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x09F8, is_global=True),
                grf.SpriteRef(0x09C1, is_global=True),
                grf.SpriteRef(0x09C9, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x09F9, is_global=True),
                grf.SpriteRef(0x09C2, is_global=True),
                grf.SpriteRef(0x09CA, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x0920, is_global=True),
                grf.SpriteRef(0x09C1, is_global=True),
                grf.SpriteRef(0x09C9, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
                grf.SpriteRef(0x0921, is_global=True),
                grf.SpriteRef(0x09C2, is_global=True),
                grf.SpriteRef(0x09CA, is_global=True),
                grf.SpriteRef(0x0, is_global=True),
            ]
        ]
        * 6,
    },
)
