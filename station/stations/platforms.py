from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetFull,
    Demo,
    ADefaultGroundSprite,
    AGroundSprite,
    AParentSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from .ground import gray


def quickload(name, symmetry, traversable):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/csps",
        voxel_getter=lambda path=f"station/voxels/csps/{name}.vox": path,
        load_from="station/files/csps-gorender.json",
        subset=symmetry.render_indices(),
    )
    sprite = symmetry.create_variants(v.spritesheet(xdiff=10))
    named_sprites[name] = sprite
    ps = AParentSprite(sprite, (16, 6, 10 if "shed" in name else 6), (0, 10, 0))
    for l, make_symmetrical, suffix in [([ps], False, ""), ([ps, ps.T], True, "_d")]:
        groundsprite = ADefaultGroundSprite(1012) if traversable else AGroundSprite(gray)
        cur_symmetry = BuildingSpriteSheetSymmetrical if make_symmetrical else symmetry
        var = cur_symmetry.get_all_variants(ALayout(groundsprite, l, True))
        layouts.extend(var)
        l = cur_symmetry.create_variants(var)
        named_tiles[name + suffix] = l


layouts = []
named_sprites = AttrDict()
named_tiles = AttrDict()

for name, symmetry, traversable in [
    ("pl1_low_white", BuildingSpriteSheetSymmetricalX, True),
    ("pl1_low_white_side", BuildingSpriteSheetSymmetricalX, False),
    ("pl1_low_white_shed", BuildingSpriteSheetSymmetricalX, True),
    ("pl1_low_white_shed_side", BuildingSpriteSheetSymmetricalX, False),
    ("pl1_low_white_shed_building", BuildingSpriteSheetFull, True),
]:
    quickload(name, symmetry, traversable)

named_tiles.globalize()

the_stations = AMetaStation(
    [
        AStation(
            id=0xF000 + i,
            translation_name="PLATFORM" if layout[0].traversable else "PLATFORM_UNTRAVERSABLE",
            layouts=layout,
            class_label=b"PLAT",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0},
        )
        for i, layout in enumerate(zip(layouts[::2], layouts[1::2]))
    ],
    b"PLAT",
    None,
    layouts,
    [
        Demo("Platform", [[pl1_low_white], [pl1_low_white_d], [pl1_low_white.T]]),
        Demo("Platform with concrete grounds", [[pl1_low_white_side], [pl1_low_white_d], [pl1_low_white_side.T]]),
        Demo("Platform with shed", [[pl1_low_white_shed], [pl1_low_white_shed_d], [pl1_low_white_shed.T]]),
    ],
)
