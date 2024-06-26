import os
import grf
from agrf.strings import get_translation
from agrf.graphics.palette import CompanyColour, company_colour_remap


cc1_remap = company_colour_remap(CompanyColour.BLUE, CompanyColour.BLUE).to_sprite()
cc2_remap = company_colour_remap(CompanyColour.WHITE, CompanyColour.RED).to_sprite()


techclass_order = [
    ("Buses", ["bus", "articulated_bus", "2decker", "coach"]),
    ("Lorries", ["l_truck", "m_truck", "h_truck"]),
    ("Urban Rail Transit", ["monorail"]),
    ("Trolleybuses", ["trolleybus"]),
]


def save_example_images(graphics_helper, prefix, file_name):
    cc1_masked_img = graphics_helper.doc_graphics(cc1_remap)
    cc1_masked_img.save(os.path.join(prefix, "img", f"{file_name}_cc1.png"))
    cc2_masked_img = graphics_helper.doc_graphics(cc2_remap)
    cc2_masked_img.save(os.path.join(prefix, "img", f"{file_name}_cc2.png"))


def metavehicle_key(mv):
    for i, (_, techclass_list) in enumerate(techclass_order):
        if mv.techclass in techclass_list:
            return i, mv.introduction_date, mv.translation_name


def gen_docs(string_manager, rosters, everything):
    for language in ["en-GB", "zh-CN"]:
        prefix = f"docs/_i18n/{language}/road_vehicle/rosters"
        os.makedirs(prefix, exist_ok=True)
        prefix = f"docs/_i18n/{language}/road_vehicle/vehicles"
        os.makedirs(prefix, exist_ok=True)

    for i, roster in enumerate(rosters):
        prefix = f"docs/road_vehicle/rosters"
        with open(os.path.join(prefix, f"{roster.translation_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {roster.name(string_manager)}
parent: Rosters
grand_parent: ACRVS - Ahyangyi's Chinese Road Vehicle Set
nav_order: {i+1}
---
{{% translate_file road_vehicle/rosters/{roster.translation_name}.md %}}
""",
                file=f,
            )

        for language in ["en-GB", "zh-CN"]:
            langprefix = f"docs/_i18n/{language}/road_vehicle/rosters"
            with open(os.path.join(langprefix, f"{roster.translation_name}.md"), "w") as f:
                for title, techclassset in techclass_order:
                    if not any(entry.techclass in techclassset for entry in roster.entries):
                        continue
                    print(
                        f"""
# {title}

| Image | Year | Name |
|-------|------|------|""",
                        file=f,
                    )
                    for entry in sorted(roster.entries, key=lambda x: x.introduction_date):
                        entry = entry.get_variants()[0]
                        if entry.techclass in techclassset:
                            name = get_translation(
                                string_manager["STR_VEHICLE_" + entry.translation_name + "_NAME"], 0x7F
                            )
                            print(
                                f"| ![](../vehicles/img/{entry.translation_name}_cc2.png) | {entry._props['introduction_date'].year} | [{name}](../vehicles/{entry.translation_name}.html)",
                                file=f,
                            )

    prefix = f"docs/road_vehicle/vehicles"
    os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
    for i, v in enumerate(sorted(everything.entries, key=metavehicle_key)):
        # Prepare text
        translation = get_translation(string_manager["STR_VEHICLE_" + v.translation_name + "_NAME"], 0x7F)
        desc_translation = get_translation(string_manager["STR_VEHICLE_" + v.translation_name + "_DESC"], 0x7F)

        # Prepare graphics
        save_example_images(v.graphics_helper, prefix, v.translation_name)

        # Dump template
        with open(os.path.join(prefix, f"{v.translation_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: Vehicles
grand_parent: ACRVS - Ahyangyi's Chinese Road Vehicle Set
nav_order: {i+1}
---

{{% translate_file road_vehicle/vehicles/{v.translation_name}.md %}}
""",
                file=f,
            )

        # Dump
        for language in ["en-GB", "zh-CN"]:
            langprefix = f"docs/_i18n/{language}/road_vehicle/vehicles"
            INTRODUCTION = {"en-GB": "Introduction", "zh-CN": "介绍"}[language]
            DATASHEET = {"en-GB": "Datasheet", "zh-CN": "数据"}[language]

            with open(os.path.join(langprefix, f"{v.translation_name}.md"), "w") as f:
                print(
                    f"""
# {INTRODUCTION}
![](img/{v.translation_name}_cc1.png)
![](img/{v.translation_name}_cc2.png)

{desc_translation}

# {DATASHEET}
## Dimensions
""",
                    file=f,
                )
                if "real_dimensions" in v:
                    print("**Dimensions**: ", v.real_dimensions_repr, file=f)

                if "variants" in v:
                    print("# Variants", file=f)
                    for variant in v.list_variants():
                        vpath = f"{v.translation_name}_{variant.id}"
                        save_example_images(variant.graphics_helper, prefix, vpath)
                        print(
                            f"""ID: {variant.id}

![](img/{vpath}_cc1.png)
![](img/{vpath}_cc2.png)

""",
                            file=f,
                        )
