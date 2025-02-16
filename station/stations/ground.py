from station.lib import BuildingSymmetrical, BuildingSymmetricalX, AGroundSprite, ALayout, AttrDict
from agrf.graphics.voxel import LazyVoxel
from station.lib.registers import Registers


def quickload(name, symmetry):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/ground",
        voxel_getter=lambda path=f"station/voxels/ground/{name}.vox": path,
        load_from="station/files/gorender.json",
        subset=symmetry.render_indices(),
    )
    v.config["agrf_manual_crop"] = (0, 0)

    sprite = symmetry.create_variants(v.spritesheet())
    ps = AGroundSprite(sprite, flags={"add": Registers.ZERO})
    named_ps[name] = ps
    l = ALayout(ps, [], False)
    named_tiles[name] = l
    return sprite


named_ps = AttrDict()
named_tiles = AttrDict()

quickload("gray", BuildingSymmetrical)
quickload("gray_third", BuildingSymmetricalX)
