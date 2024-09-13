from station.lib import (
    AStation,
    AMetaStation,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetrical,
    Demo,
    ADefaultGroundSprite,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
    Registers,
    get_1cc_remap,
)
from agrf.graphics.voxel import LazyVoxel
from station.lib.parameters import station_cb
from .misc import building_ground
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from agrf.graphics.palette import CompanyColour


def quickload(name, symmetry):
    v = LazyVoxel(
        name,
        prefix="station/voxels/render/dovemere_1934",
        voxel_getter=lambda path=f"station/voxels/dovemere_1934/{name}.vox": path,
        load_from="station/files/gorender.json",
        config={"agrf_palette": "station/files/dovemere_1934_palette.json", "z_scale": 1.0},
        subset=symmetry.render_indices(),
    )
    building = v.discard_layers(("snow",), "building")
    snow = v.discard_layers(("building",), "snow")
    snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)

    building.config["agrf_manual_crop"] = (0, 10)
    snow.config["agrf_childsprite"] = (0, -10)

    sprite = symmetry.create_variants(building.spritesheet(xdiff=1, xspan=8))
    ps = AParentSprite(sprite, (16, 8, 16), (0, 0, 0))
    snow_sprite = symmetry.create_variants(snow.spritesheet())
    cs = AChildSprite(snow_sprite, (0, 0), flags={"dodraw": Registers.SNOW})

    l = ALayout(building_ground, [ps + cs], False)
    var = symmetry.get_all_variants(l)
    ret = symmetry.create_variants(var)
    entries.extend(symmetry.get_all_entries(ret))
    named_tiles[name] = ret


entries = []
named_tiles = AttrDict()
for name, symmetry in [("regular", BuildingSpriteSheetSymmetricalX)]:
    quickload(name, symmetry)

station_tiles = []
for i, entry in enumerate(entries):
    station_tiles.append(
        AStation(
            id=0x2000 + i,
            translation_name="PLATFORM" if entry.traversable else "PLATFORM_UNTRAVERSABLE",
            layouts=[entry, entry.M],
            class_label=b"\xe8\x8a\x9c0",
            cargo_threshold=40,
            callbacks={"select_tile_layout": 0, **station_cb["E88A9C0"]},
            doc_layout=entry,
        )
    )

the_stations = AMetaStation(
    station_tiles,
    b"\xe8\x8a\x9c0",
    None,
    [
        Demo("The building", [[named_tiles.regular]]),
        Demo(
            "With snow",
            [[named_tiles.regular]],
            remap=get_1cc_remap(CompanyColour.PINK),
            climate="arctic",
            subclimate="snow",
        ),
    ],
)
