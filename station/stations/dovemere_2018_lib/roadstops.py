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


for name, sym in [
    ("overpass", BuildingSpriteSheetSymmetricalX),
    ("west_stair", BuildingSpriteSheetFull),
    ("west_stair_extender", BuildingSpriteSheetSymmetricalX),
]:
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
        # config={"z_scale": 1.01},
    )
    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(v.spritesheet())
    ps = AParentSprite(sprite, (16, 16, 12), (0, 0, 0))
    layout = ALayout(road_ground, [ps], True, category=b"\xe8\x8a\x9cR")

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
