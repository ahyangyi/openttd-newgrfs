from agrf.graphics.voxel import LazyVoxel
from station.lib import (
    BuildingFull,
    AParentSprite,
    AChildSprite,
    AttrDict,
    Registers,
)
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR


components = AttrDict(schema=("name",))


def make_component(name, sym):
    v = LazyVoxel(
        name,
        prefix=f".cache/render/csl/{dirname}",
        voxel_getter=lambda path=f"csl/voxels/{name}.vox": path,
        load_from="csl/files/cns-gorender.json",
    )

    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(
        v.spritesheet()
    )
    components[(name,)] = gs


def make_components():
    make_component("tiny", BuildingFull)
