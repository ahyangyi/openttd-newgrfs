import grf
from station.lib import (
    BuildingFull,
    BuildingSymmetricalX,
    BuildingSymmetrical,
    BuildingCylindrical,
    BuildingDiamond,
    BuildingDiagonalAlt,
    BuildingRotational4,
    AGroundSprite,
    AParentSprite,
    AChildSprite,
    ALayout,
    AttrDict,
    Registers,
    Demo,
)
from grfobject.lib import AObject, GraphicalSwitch, PositionSwitch
from agrf.graphics.recolour import NON_RENDERABLE_COLOUR
from agrf.lib.building.slope import make_slopes, slope_types

DEFAULT_FLAGS = grf.Object.Flags.ONLY_IN_GAME | grf.Object.Flags.ALLOW_UNDER_BRIDGE
DEFAULT_SLOPE_FLAGS = DEFAULT_FLAGS | grf.Object.Flags.AUTOREMOVE | grf.Object.Flags.HAS_NO_FOUNDATION

named_layouts = AttrDict(schema=("name", "offset"))
objects = []


def register_slopes(slopes, sym, starting_id, flags=DEFAULT_SLOPE_FLAGS):
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
            id=starting_id,
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
        starting_id += 1
        objects.append(cur_object)


def register(layouts, sym, label, starting_id, flags=DEFAULT_FLAGS, allow_flip=True):
    rows = len(layouts)
    columns = len(layouts[0])
    layout = PositionSwitch(
        ranges={r * 256 + c: layouts[r][c] for r in range(rows) for c in range(columns)},
        default=layouts[0][0],
        code="relative_pos",
        rows=rows,
        columns=columns,
    )
    for cur in sym.chiralities(layout)[: 2 if allow_flip else 1]:
        demo = Demo(cur.to_lists())
        doc_layout = demo.to_layout()
        doc_layout.category = b"\xe8\x8a\x9cZ"  # FIXME doc category?
        layouts = sym.rotational_views(cur)
        num_views = len(layouts)
        cur_object = AObject(
            id=starting_id,
            translation_name="WEST_PLAZA",
            layouts=layouts,
            purchase_layouts=sym.rotational_views(doc_layout),
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
        starting_id += 1
        objects.append(cur_object)
