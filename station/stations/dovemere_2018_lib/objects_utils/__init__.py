from grfobject.lib import AObject, GraphicalSwitch
from station.lib import AttrDict
import grf
from agrf.lib.building.slope import slope_types

DEFAULT_FLAGS = grf.Object.Flags.ONLY_IN_GAME | grf.Object.Flags.ALLOW_UNDER_BRIDGE
DEFAULT_SLOPE_FLAGS = DEFAULT_FLAGS | grf.Object.Flags.AUTOREMOVE | grf.Object.Flags.HAS_NO_FOUNDATION

named_layouts = AttrDict(schema=("name", "offset"))
objects = []


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
