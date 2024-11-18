import grf
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    BuildingCylindrical,
    BuildingDiamond,
    BuildingDiagonalAlt,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
    Registers,
    Demo,
)
from agrf.graphics.voxel import LazyVoxel
from grfobject.lib import AObject, GraphicalSwitch, PositionSwitch
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from agrf.lib.building.slope import make_slopes, slope_types
from .west_plaza.grounds import named_grounds

DEFAULT_FLAGS = grf.Object.Flags.ONLY_IN_GAME | grf.Object.Flags.ALLOW_UNDER_BRIDGE
DEFAULT_SLOPE_FLAGS = DEFAULT_FLAGS | grf.Object.Flags.AUTOREMOVE | grf.Object.Flags.HAS_NO_FOUNDATION

named_layouts = AttrDict(schema=("name", "offset"))
objects = []


def register(layouts, sym, label, flags=DEFAULT_FLAGS):
    rows = len(layouts)
    columns = len(layouts[0])
    layout = PositionSwitch(
        ranges={r * 256 + c: layouts[r][c] for r in range(rows) for c in range(columns)},
        default=layouts[0][0],
        code="relative_pos",
        rows=rows,
        columns=columns,
    )
    for cur in sym.chiralities(layout):
        demo = Demo("", cur.to_lists())
        doc_layout = demo.to_layout()
        doc_layout.category = b"\xe8\x8a\x9cZ"  # FIXME doc category?
        layouts = sym.rotational_views(cur)
        num_views = len(layouts)
        cur_object = AObject(
            id=len(objects),
            translation_name="WEST_PLAZA",
            layouts=layouts,
            purchase_layouts=layouts,
            class_label=b"\xe8\x8a\x9c" + label,
            climates_available=grf.ALL_CLIMATES,
            size=(columns, rows),
            num_views=num_views,
            introduction_date=0,
            end_of_life_date=0,
            height=1,
            flags=flags,
            doc_layout=doc_layout,
            callbacks={"tile_check": 0x400},
        )
        objects.append(cur_object)


def register_slopes(slopes, sym, flags=DEFAULT_SLOPE_FLAGS):
    for chi_ind in sym.chirality_indices():
        layouts = []
        purchase_layouts = []
        for view_ind in sym.rotational_view_indices():
            ranges = {}
            for slope_type in slope_types:
                cur = slopes[sym.canonical_index(chi_ind ^ view_ind)][slope_type]
                ranges[slope_type] = cur
            default = ranges.pop(0)
            switch = GraphicalSwitch(ranges=ranges, default=default, code="tile_slope")

            layouts.append(switch)
            purchase_layouts.append(default)

        cur_object = AObject(
            id=len(objects),
            translation_name="WEST_PLAZA",
            layouts=layouts,
            purchase_layouts=purchase_layouts,
            class_label=b"\xe8\x8a\x9cG",
            climates_available=grf.ALL_CLIMATES,
            size=(1, 1),
            num_views=len(layouts),
            introduction_date=0,
            end_of_life_date=0,
            height=1,
            flags=flags,
            doc_layout=purchase_layouts[0],
            callbacks={"tile_check": 0x400},
        )
        objects.append(cur_object)


def make_ground_layout(name, sym):
    gs = named_grounds[(name, "")]
    layout = ALayout(gs, [], True, category=b"\xe8\x8a\x9cZ")

    slopes = make_slopes(
        {
            i: ALayout(named_grounds[(name, str(i) if i > 0 else "")], [], True, category=b"\xe8\x8a\x9cZ")
            for i in slope_types
        },
        sym,
    )

    named_layouts[(name, "")] = layout
    register_slopes(slopes, sym)


make_ground_layout("west_plaza_center", BuildingSymmetrical)
make_ground_layout("west_plaza_offcenter_A", BuildingFull)
make_ground_layout("west_plaza_offcenter_B", BuildingFull)
make_ground_layout("west_plaza_diagonal", BuildingDiamond)
make_ground_layout("west_plaza_checkerboard", BuildingCylindrical)

all_layers = (
    "edge marker",
    "flowers 1",
    "flowers 2",
    "flowers 3",
    "flowers 4",
    "flowers 5",
    "flowers 6",
    "flowers 7",
    "houses",
    "arcs",
    "xiangqi pieces",
    "basket",
    "bouquet",
    "bushes",
    "ruyi",
)


def make_object_layout(name, sym, Xspan, Yspan, xspan, yspan, height, osym=None):
    if osym is None:
        osym = sym

    gs = named_grounds[("west_plaza_center", "")]
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    snow = v.discard_layers(("ground snow",) + all_layers, "snow")
    snow = snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    snow.config["agrf_childsprite"] = (0, -11)
    snow.in_place_subset(osym.render_indices())
    snowsprite = osym.create_variants(snow.spritesheet())

    ground_snow = v.discard_layers(("snow",) + all_layers, "ground_snow")
    ground_snow = ground_snow.compose(v, "merge", ignore_mask=True, colour_map=NON_RENDERABLE_COLOUR)
    ground_snow.config["agrf_childsprite"] = (0, -10)
    ground_snow.in_place_subset(sym.render_indices())
    ground_snowsprite = sym.create_variants(ground_snow.spritesheet())

    v = v.discard_layers(("snow", "ground snow"), "nosnow")
    ground = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_ground_mask.vox", "ground")
    ground.config["agrf_manual_crop"] = (0, 10)
    ground.in_place_subset(sym.render_indices())
    groundsprite = sym.create_variants(ground.spritesheet())

    gscs = AChildSprite(groundsprite, (0, 0))
    ground_snowcs = AChildSprite(ground_snowsprite, (0, 0), flags={"dodraw": Registers.SNOW})
    gs2 = gs + gscs + ground_snowcs

    xofs = (16 - xspan) // 2
    yofs = (16 - yspan) // 2
    Xofs = (16 - Xspan) // 2
    Yofs = (16 - Yspan) // 2

    v = v.mask_clip_away("station/voxels/dovemere_2018/masks/object_mask.vox", "object")
    v.config["agrf_manual_crop"] = (0, 11)
    v.in_place_subset(osym.render_indices())
    sprite = osym.create_variants(v.spritesheet(xdiff=xofs, xspan=xspan, ydiff=yofs, yspan=yspan, zdiff=1))
    snowcs = AChildSprite(snowsprite, (0, 0), flags={"dodraw": Registers.SNOW})

    # ps = [AParentSprite(sprite, (yspan, xspan, height), (yofs, xofs, 0)) + snowcs]
    # layout = ALayout(gs2, ps, True, category=b"\xe8\x8a\x9cZ")
    # named_layouts[(name, "grounded")] = layout
    # register(layout, sym, b'F')

    gl = named_layouts[("west_plaza_center", "")]

    groundsprite2 = sym.create_variants(ground.spritesheet(xdiff=Xofs, xspan=Xspan, ydiff=Yofs, yspan=Yspan))
    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "")] = layout
    register([[layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs - 4, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs - 4, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "half")] = layout
    register([[layout]], sym.break_y_symmetry(), b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs, Xofs - 8, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs, xofs - 8, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "vertical")] = layout
    register([[gl], [layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "horizontal")] = layout
    register([[gl, layout]], sym, b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs - 4, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs - 4, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "half_horizontal")] = layout
    register([[gl, layout]], sym.break_y_symmetry(), b"F")

    ps = [
        AParentSprite(groundsprite2, (Yspan, Xspan, 1), (Yofs - 8, Xofs - 8, 0)) + ground_snowcs,
        AParentSprite(sprite, (yspan, xspan, height - 1), (yofs - 8, xofs - 8, 1)) + snowcs,
    ]
    layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
    named_layouts[(name, "corner")] = layout
    register([[gl, gl], [gl, layout]], sym, b"F")


make_object_layout("west_plaza_center_flower_2021", BuildingSymmetrical, 8, 10, 4, 8, 6)
make_object_layout("west_plaza_center_flower_2022", BuildingSymmetrical, 8, 10, 4, 8, 6)
make_object_layout("west_plaza_center_flower_2023", BuildingSymmetrical, 6, 16, 2, 10, 10)
make_object_layout("west_plaza_center_flower_2024", BuildingSymmetrical, 8, 12, 2, 2, 6, BuildingCylindrical)


def object_part(name, sym, span, offset):
    v = LazyVoxel(
        name,
        prefix=".cache/render/station/dovemere_2018/plaza",
        voxel_getter=lambda path=f"station/voxels/dovemere_2018/plaza/{name}.vox": path,
        load_from="station/files/cns-gorender.json",
    )
    v.config["agrf_manual_crop"] = (0, 10)
    v.config["agrf_palette"] = "station/files/cns-palette-hard.json"
    v.in_place_subset(sym.render_indices())
    sprite = sym.create_variants(
        v.spritesheet(xspan=span[1], yspan=span[0], xdiff=offset[1], ydiff=offset[0], zdiff=offset[2])
    )
    gs = AParentSprite(sprite, span, offset)
    return gs


planter_1 = object_part("west_plaza_planter_1", BuildingFull, (4, 4, 1), (2, 10, 0)).move(-4, 0)
planter_2 = object_part("west_plaza_planter_2", BuildingFull, (7, 4, 1), (2, 10, 0))
pole = object_part("west_plaza_pole", BuildingSymmetrical, (2, 2, 8), (7, 7, 0))
underground_entrance = object_part("west_plaza_underground_entrance", BuildingFull, (4, 4, 8), (6, 6, 0)).move(6, -6)
corner_lawn = object_part("corner_lawn", BuildingDiagonalAlt, (6, 6, 1), (10, 0, 0))
edge_lawn = object_part("edge_lawn", BuildingSymmetricalX, (16, 6, 1), (0, 0, 0))
split_lawn = object_part("split_lawn", BuildingFull, (16, 6, 1), (0, 10, 0))

gs = named_grounds[("west_plaza_offcenter_B", "")]
ps = [
    planter_1,
    planter_2,
    pole.move(-2, 0),
    pole.move(2, 0),
    pole.move(-2, -4),
    pole.move(2, -4),
    underground_entrance,
]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_B", "decorated")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8)]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_A", "decorated")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 4), pole.move(2, 4), pole.move(-2, 8), pole.move(2, 8), corner_lawn]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_A", "decorated_lawn")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_offcenter_A", "")]
ps = [pole.move(-2, 0), pole.move(2, 0), pole.move(-2, 4), pole.move(2, 4), underground_entrance.move(0, 8)]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_offcenter_B", "oneliner")] = layout
register([[layout]], BuildingFull, b"L")

gs = named_grounds[("west_plaza_center", "")]
ps = [edge_lawn]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_center", "lawn")] = layout
register([[layout]], BuildingSymmetricalX, b"L")

gs = named_grounds[("west_plaza_center", "")]
ps = [split_lawn]
layout = ALayout(gs, ps, True, category=b"\xe8\x8a\x9cZ")
named_layouts[("west_plaza_center", "split_lawn")] = layout
register([[layout]], BuildingSymmetricalX, b"L")
