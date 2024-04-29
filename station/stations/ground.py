from station.lib import (
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    AGroundSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel


def quickload(name, type):
    ret = []
    for i in range(3):
        v = LazyVoxel(
            name,
            prefix="station/voxels/render/ground",
            voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
            load_from="station/files/gorender.json",
            subset=type.render_indices(),
        )

        sprite = type.create_variants(v.spritesheet())
        ret.append(sprite)
    ps = AGroundSprite(ret[0], alternatives=ret[1:])
    named_ps[name] = ps
    l = ALayout([ps], [], False)
    named_tiles[name] = l
    return sprite, ps, l


named_ps = AttrDict()
named_tiles = AttrDict()
((gray, gray_ps, gray_layout), (gray_third, gray_third_ps, gray_third_layout)) = [
    quickload(name, type)
    for name, type in [("gray", BuildingSpriteSheetSymmetrical), ("gray_third", BuildingSpriteSheetSymmetricalX)]
]
