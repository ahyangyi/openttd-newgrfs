import os
import math
import grf
from tabulate import tabulate
from road_vehicle.lib import ARoadVehicle, supported_techclasses
from agrf.strings import get_translation
from agrf.graphics.blend import blend
from agrf.graphics.palette import CompanyColour, company_colour_remap


def dimens_repr(dimensions):
    if dimensions is None:
        return ""
    return " × ".join(map(str, dimensions))


def ceil_sign(x):
    return str(math.ceil(x)) + ("-" if math.ceil(x) - x > 0.5 else "")


def round_sign(x):
    return str(int(x + 0.5)) + ("+" if x > int(x + 0.5) else "-")


class Roster:
    def __init__(self, *entries):
        self.entries = entries
        variants = [y for x in entries for y in x.variant.get_variants()]
        self.rvs = list(sorted(variants, key=lambda x: supported_techclasses.index(x.techclass)))

    def register(self, grf):
        for rv in self.rvs:
            grf.add(rv)

    def gameplay_table(self):
        ret = []
        for rv in self.rvs:
            if not isinstance(rv, ARoadVehicle):
                continue
            ret.append(
                (
                    rv.name,
                    rv._props["introduction_date"].year,
                    rv.real_speed(),
                    rv._props["cargo_capacity"],
                    f"{ARoadVehicle.ton_from_weight(rv.weight_empty)}, "
                    + f"{ARoadVehicle.ton_from_weight(rv.weight_empty) + rv.capacity_in_tons}",
                    rv.tractive_effort() / 1000,
                    rv.power_in_hp(),
                    rv.first_gear_speed(),
                    sorted(list(rv.tags)),
                    rv.techclass,
                )
            )
        return ret

    @staticmethod
    def gameplay_header():
        return [
            "Name",
            "Year",
            "Speed",
            "Capacity",
            "Weight",
            "Tractive Effort",
            "Horsepower",
            "First Gear Speed",
            "Tags",
            "Tech Class",
        ]

    def gameplay_cli(self):
        return tabulate(self.gameplay_table(), self.gameplay_header())

    def hogscost_table(self):
        ret = []
        for rv in self.rvs:
            if not isinstance(rv, ARoadVehicle):
                continue
            ret.append(
                (
                    rv.name,
                    rv.hog_power_points,
                    rv.hog_speed_points,
                    rv.hog_date_points,
                    rv.hog_capacity_points,
                    rv.hog_points,
                )
            )
        return ret

    @staticmethod
    def hogscost_header():
        return [
            "Name",
            "Power",
            "Speed",
            "Date",
            "Capacity",
            "Hog Points",
        ]

    def hogscost_cli(self):
        return tabulate(self.hogscost_table(), self.hogscost_header())

    def dimension_table(self):
        ret = []
        for rv in self.rvs:
            if not isinstance(rv, ARoadVehicle):
                continue
            ret.append((rv.name, dimens_repr(rv.real_dimensions), rv.real_x_dimensions, rv.axle_track, rv.tire))
        return ret

    @staticmethod
    def dimension_header():
        return [
            "Name",
            "Dimension",
            "FOverhang / Wheelbase / ROverhang",
            "Axle Track",
            "Tire",
        ]

    def dimension_cli(self):
        return tabulate(self.dimension_table(), self.dimension_header())

    def in_game_dimension_table(self):
        ret = []
        for rv in self.rvs:
            if not isinstance(rv, ARoadVehicle):
                continue
            try:
                l, w, h = rv.real_dimensions
                prop_in_game_dim = int(l / 0.0458 + 0.5), int(w / 0.0347 + 0.5), int(h / 0.0458 + 0.5)
                L = ceil_sign(l / 0.0458 / 26)
            except:
                prop_in_game_dim = None
                L = None

            if rv.real_x_dimensions is None:
                x_dimensions = None
            else:
                x_dimensions = []
                tot = 0
                for x in rv.real_x_dimensions[:-1]:
                    tot += x
                    pos = tot / 0.0458
                    x_dimensions.append(round_sign(pos))

            if rv.tire is None:
                tire_dimens = None
            else:
                tire_diameter = int(rv.tire.diameter / 1000 / 0.0458 + 0.5)
                tire_width = int(rv.tire.width / 1000 / 0.0347 + 0.5)
                tire_dimens = (tire_diameter, tire_width)

            if rv.axle_track is None:
                axle_track = None
            else:
                axle_track = [round(x / 0.0347) for x in rv.axle_track]

            ret.append(
                (
                    rv.name,
                    dimens_repr(rv.voxel_dimensions),
                    dimens_repr(prop_in_game_dim),
                    L,
                    x_dimensions,
                    axle_track,
                    dimens_repr(tire_dimens),
                )
            )
        return ret

    @staticmethod
    def in_game_dimension_header():
        return [
            "Name",
            "Dimension",
            "Dimension (prop.)",
            "Length (prop.)",
            "Axle Coordination",
            "Axle Track",
            "Tire Dimension (prop.)",
        ]

    def in_game_dimension_cli(self):
        return tabulate(self.in_game_dimension_table(), self.in_game_dimension_header())

    def cli(self):
        return "\n\n".join(
            [
                self.gameplay_cli(),
                self.hogscost_cli(),
                self.dimension_cli(),
                self.in_game_dimension_cli(),
            ]
        )

    def gen_docs(self, string_manager):
        prefix = "docs/road_vehicle/vehicles"
        os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
        cc1_remap = company_colour_remap(CompanyColour.BLUE, CompanyColour.BLUE).to_sprite()
        cc2_remap = company_colour_remap(CompanyColour.WHITE, CompanyColour.RED).to_sprite()
        for i, entry in enumerate(self.entries):
            # Prepare text
            v = entry.variant
            translation = get_translation(string_manager["STR_RV_" + v["translation_name"] + "_NAME"], 0x7F)
            desc_translation = get_translation(string_manager["STR_RV_" + v["translation_name"] + "_DESC"], 0x7F)

            # Prepare graphics
            sprite = v.graphics_helper.doc_graphics()
            masked_sprite = sprite.get_zoom_bpp(grf.ZOOM_NORMAL, 32)
            img, _ = masked_sprite.get_image()
            mask, _ = masked_sprite.mask.get_image()
            cc1_mask = cc1_remap.remap_image(mask)
            cc1_masked_img = blend(img, cc1_mask)
            cc1_masked_img.save(os.path.join(prefix, "img", f'{v["translation_name"]}_cc1.png'))
            cc2_mask = cc2_remap.remap_image(mask)
            cc2_masked_img = blend(img, cc2_mask)
            cc2_masked_img.save(os.path.join(prefix, "img", f'{v["translation_name"]}_cc2.png'))

            # Dump
            with open(os.path.join(prefix, f'{v["translation_name"]}.md'), "w") as f:
                print(
                    f"""---
layout: default
title: {translation}
parent: Vehicles
grand_parent: Ahyangyi's Road Vehicles (ARV)
nav_order: {i+1}
---
# Introduction
![](img/{v["translation_name"]}_cc1.png)
![](img/{v["translation_name"]}_cc2.png)
{desc_translation}

# Datasheet
""",
                    file=f,
                )
