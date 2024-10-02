from station.lib import BuildingSymmetrical, BuildingSymmetricalX, AGroundSprite, ALayout, AttrDict
from agrf.graphics.voxel import LazyVoxel
from station.lib.registers import Registers


def quickload(name, type):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=type.render_indices(),
    )

    sprite = type.create_variants(v.spritesheet())
    ps = AGroundSprite(sprite, flags={"add": Registers.ZERO})
    named_ps[name] = ps
    l = ALayout(ps, [], False)
    named_tiles[name] = l
    return sprite


named_ps = AttrDict()
named_tiles = AttrDict()
gray, gray_third = [
    quickload(name, type) for name, type in [("gray", BuildingSymmetrical), ("gray_third", BuildingSymmetricalX)]
]
