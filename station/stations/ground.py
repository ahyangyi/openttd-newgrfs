from station.lib import BuildingSpriteSheetSymmetrical, BuildingSpriteSheetSymmetricalX
from agrf.graphics.voxel import LazyVoxel


def quickload(name, type):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )
    sprite = type.create_variants(v.spritesheet())
    sprites.extend(sprite.all_variants)
    return sprite


sprites = []
(gray, gray_third) = [
    quickload(name, type)
    for name, type in [("gray", BuildingSpriteSheetSymmetrical), ("gray_third", BuildingSpriteSheetSymmetricalX)]
]