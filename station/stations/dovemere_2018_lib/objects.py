import grf
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    BuildingCylindrical,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
)
from agrf.graphics.voxel import LazyVoxel
from grfobject.lib import AObject

named_grounds = AttrDict(schema=("name"))
named_layouts = AttrDict(schema=("name", "offset"))
objects = []

for name, sym in [("west_plaza_center", BuildingSymmetrical), ("west_plaza_offcenter", BuildingFull)]:
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


def register(layout, sym):
    for cur in [layout, layout.R] if (sym is BuildingFull) else [layout]:
        if sym is BuildingSymmetrical:
            layouts = [cur, cur.R.M]
            num_views = 2
        else:
            layouts = [cur, cur.T.M, cur.R.M, cur.T.R]
            num_views = 4
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


def make_ground_layout(name, sym):
    gs = named_grounds[(name,)]
    layout = ALayout(gs, [], True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "")] = layout
    register(layout, sym)


make_ground_layout("west_plaza_center", BuildingSymmetrical)
make_ground_layout("west_plaza_offcenter", BuildingFull)


def make_object_layout(name, sym, Xspan, Yspan, xspan, yspan, height, osym=None):
    if osym is None:
        osym = sym

    gs = named_grounds[("west_plaza_center",)]
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    v = v.discard_layers(("snow",), "nosnow")
    ground = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_ground_mask.vox", "ground")
    ground.in_place_subset(sym.render_indices())
    groundsprite = sym.create_variants(ground.spritesheet())
    gscs = AChildSprite(groundsprite, (0, 0))
    gs2 = gs + gscs

    xofs = (16 - xspan) // 2
    yofs = (16 - yspan) // 2
    Xofs = (16 - Xspan) // 2
    Yofs = (16 - Yspan) // 2

    v = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_mask.vox", "object")
    v.in_place_subset(osym.render_indices())

    sprite = osym.create_variants(v.spritesheet(xdiff=xofs, xspan=xspan, ydiff=yofs, yspan=yspan))

    ps = [AParentSprite(sprite, (yspan, xspan, height), (yofs, xofs, 0))]
    layout = ALayout(gs2, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "")] = layout
    register(layout, sym)

    groundsprite2 = sym.create_variants(ground.spritesheet(xdiff=Xofs, xspan=Xspan, ydiff=Yofs, yspan=Yspan))
    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 0), (Yofs, Xofs - 8, 0)),
        AParentSprite(sprite, (yspan, xspan, height), (yofs, xofs - 8, 0)),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "vertical")] = layout
    register(layout, sym.break_y_symmetry())

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 0), (Yofs - 8, Xofs, 0)),
        AParentSprite(sprite, (yspan, xspan, height), (yofs - 8, xofs, 0)),
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "horizontal")] = layout
    register(layout, sym.break_x_symmetry())


make_object_layout("west_plaza_center_flower_2021", BuildingSymmetrical, 8, 10, 4, 8, 6)
make_object_layout("west_plaza_center_flower_2022", BuildingSymmetrical, 8, 10, 4, 8, 6)
make_object_layout("west_plaza_center_flower_2023", BuildingSymmetrical, 6, 16, 2, 10, 6)
make_object_layout("west_plaza_center_flower_2024", BuildingSymmetrical, 8, 12, 2, 2, 6, BuildingCylindrical)
