from dataclass import dataclass
from .symmetry import BuildingSymmetricalX, BuildingDiamond, BuildingCylindrical, BuildingDiagonalAlt, BuildingDiagonal


@dataclass
class SlopeType:
    slope_type: int


flat = BuildingCylindrical.create_variants(SlopeType(0))
ortho = BuildingSymmetricalX.create_variants(SlopeType(3), SlopeType(9), SlopeType(12), SlopeType(6))
para = BuildingDiamond.create_variants(SlopeType(5), SlopeType(10))
mono = BuildingDiagonalAlt.create_variants(SlopeType(1), SlopeType(2), SlopeType(8), SlopeType(4))
tri = BuildingDiagonal.create_variants(SlopeType(7), SlopeType(14), SlopeType(13), SlopeType(11))
steep = BuildingDiagonal.create_variants(SlopeType(23), SlopeType(30), SlopeType(27), SlopeType(29))


def make_slopes(sprites, sym):
    for slopeGroup in [flat, ortho, para, mono, tri, steep]:
        pass


def register(layout, sym, flags=grf.Object.Flags.ONLY_IN_GAME):
    for cur in sym.chiralities(layout):
        purchase = cur
        while isinstance(purchase, GraphicalSwitch):
            purchase = purchase.default
        layouts = sym.rotational_views(cur)
        purchase_layouts = sym.rotational_views(purchase)
        num_views = len(layouts)
        cur_object = AObject(
            id=len(objects),
            translation_name="WEST_PLAZA",
            layouts=layouts,
            purchase_layouts=purchase_layouts,
            class_label=b"\xe8\x8a\x9cZ",
            climates_available=grf.ALL_CLIMATES,
            size=(1, 1),
            num_views=num_views,
            introduction_date=0,
            end_of_life_date=0,
            height=1,
            flags=flags,
            doc_layout=purchase,
            callbacks={"tile_check": 0x400},
        )
        objects.append(cur_object)


def make_ground_layout(name, sym):
    gs = named_grounds[(name, "")]
    layout = ALayout(gs, [], True, category=b"\xe8\x8a\x9cZ")

    ranges = {}
    for slope_type in [1, 2, 4, 8, 5, 10, 3, 6, 9, 12, 7, 11, 13, 14, 23, 27, 29, 30]:
        gs2 = named_grounds[(name, str(slope_type))]
        layout2 = ALayout(gs2, [], True)
        ranges[slope_type] = layout2

    s = GraphicalSwitch(ranges=ranges, default=layout, code="tile_slope")
    named_layouts[(name, "")] = layout
    register(s, sym, flags=grf.Object.Flags.ONLY_IN_GAME | grf.Object.Flags.HAS_NO_FOUNDATION)
