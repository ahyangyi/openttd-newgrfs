from agrf.graphics.voxel import LazyVoxel, LazySpriteSheet


def get_spritesheet(name):
    voxels = [
        LazyVoxel(
            k,
            prefix=f".cache/render/road/{name}",
            voxel_getter=lambda k=k: f"road/voxels/{name}/{k}.vox",
            load_from="road/render_templates/gorender.json",
        )
        for k in ["straight", "crossroad", "junction", "curve", "end"]
    ]
    # XXX: logically this should be 32 * 2**0.5 / 8 / (3**0.5 / 2)
    # but it doesn't really fit
    voxels.append(voxels[0].stairstep(32 * 2**0.5 / 8, "hill"))
    spritesheet = LazySpriteSheet(
        voxels,
        [
            (0, 1),
            (0, 0),
            (1, 0),
            (2, 3),
            (2, 2),
            (2, 1),
            (2, 0),
            (3, 3),
            (3, 0),
            (3, 1),
            (3, 2),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
            (4, 3),
            (4, 0),
            (4, 1),
            (4, 2),
        ],
    )
    return spritesheet.spritesheet()
