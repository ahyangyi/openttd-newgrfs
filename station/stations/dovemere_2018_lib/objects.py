import grf
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from grfobject.lib import AObject

named_grounds = AttrDict(schema=("name"))
named_layouts = AttrDict(schema=("name"))
objects = []

for name, sym in [("west_plaza_center", BuildingSymmetrical)]:
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(v.spritesheet())
    gs = AGroundSprite(sprite)
    named_grounds[(name,)] = gs

for name, sym in [
    ("west_plaza_center", BuildingSymmetrical),
    ("west_plaza_center_flower_2021", BuildingSymmetrical),
    ("west_plaza_center_flower_2022", BuildingSymmetrical),
    ("west_plaza_center_flower_2023", BuildingSymmetrical),
    ("west_plaza_center_flower_2024", BuildingSymmetrical),
]:
    if name == "west_plaza_center":
        ps = []
    else:
        v = LazyVoxel(
            name,
            prefix=".cache/render/station/dovemere_2018/plaza",
            voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
            load_from="station/files/cns-gorender.json",
        )
        v = v.discard_layers(("snow",), "nosnow")
        v.in_place_subset(sym.render_indices())
        sprite = sym.create_variants(v.spritesheet())
        ps = [AParentSprite(sprite, (16, 16, 12), (0, 0, 0))]
    gs = named_grounds[("west_plaza_center",)]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")

    for cur in [layout, layout.R] if (sym is BuildingFull) else [layout]:
        if sym is BuildingSymmetrical:
            layouts = [cur, cur.M]
            num_views = 2
        cur_object = AObject(
            id=len(objects),
            translation_name="WEST_PLAZA",
            layouts=layouts,
            class_label=b"\xe8\x8a\x9cZ",
            climates_available=grf.ALL_CLIMATES,
            size=(1, 1),
            num_views=num_views,
            introduction_date=0,
            end_of_life_date=0,
            height=1,
            flags=grf.Object.Flags.ONLY_IN_GAME,
            doc_layout=cur,
        )
        objects.append(cur_object)
