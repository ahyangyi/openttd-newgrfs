import grf
from station.lib import (
    BuildingFull,
    BuildingSymmetrical,
    BuildingCylindrical,
    BuildingDiamond,
    AttrDict,
    AGroundSprite,
    ALayout,
)
from agrf.graphics.voxel import LazyVoxel
from agrf.lib.building.slope import make_slopes, slope_types
from ..objects_utils import register, register_slopes, named_layouts

DEFAULT_FLAGS = grf.Object.Flags.ONLY_IN_GAME | grf.Object.Flags.ALLOW_UNDER_BRIDGE
DEFAULT_SLOPE_FLAGS = DEFAULT_FLAGS | grf.Object.Flags.AUTOREMOVE | grf.Object.Flags.HAS_NO_FOUNDATION

named_grounds = AttrDict(schema=("name", "slope"))

for name, sym in [("center", BuildingSymmetrical)]:
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/west_plaza/ground",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/west_plaza/ground/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    v.config["agrf_palette"] = "station/files/cns-palette-ground.json"
    v.config["agrf_bpps"] = [8]

    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(v.spritesheet())
    named_grounds[(name, "")] = AGroundSprite(sprite)

    for slope_type in [1, 2, 4, 8, 5, 10, 3, 6, 9, 12, 7, 11, 13, 14, 23, 27, 29, 30]:
        v2 = v.update_config({"slope": 8 / (32 * 2**0.5), "slope_type": slope_type}, str(slope_type))
        v2.in_place_subset(sym.render_indices())
        sprite2 = sym.create_variants(v2.spritesheet())
        named_grounds[(name, str(slope_type))] = AGroundSprite(sprite2)


def make_ground_layout(name, sym, starting_id):
    gs = named_grounds[(name, "")]
    layout = ALayout(gs, [], True, category=b"\xe8\x8a\x9cZ")

    slopes = make_slopes(
        {
            i: ALayout(named_grounds[(name, str(i) if i > 0 else "")], [], True, category=b"\xe8\x8a\x9cZ")
            for i in slope_types
        },
        sym,
    )

    named_layouts[("west_plaza_" + name, "")] = layout
    register_slopes(slopes, sym, starting_id)
    register([[layout]], sym, b"g", starting_id + 0x80)


def make_ground_layouts():
    make_ground_layout("center", BuildingSymmetrical, 0x0)
