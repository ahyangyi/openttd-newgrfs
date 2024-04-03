from station.lib import BuildingSpriteSheetSymmetrical, BuildingSpriteSheetSymmetricalX, AGroundSprite, ALayout
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
    l = ALayout(AGroundSprite(sprite), [], False)
    return sprite, l


sprites = []
((gray, gray_layout), (gray_third, gray_third_layout)) = [
    quickload(name, type)
    for name, type in [("gray", BuildingSpriteSheetSymmetrical), ("gray_third", BuildingSpriteSheetSymmetricalX)]
]
