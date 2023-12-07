import os
import grf
from agrf.strings import get_translation
from agrf.graphics.blend import blend
from agrf.graphics.palette import CompanyColour, company_colour_remap


def gen_docs(string_manager, rosters):
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
                print(
                    f"""
# Buses

| Year  | Name |
|-------|------|""",
                    file=f,
                )
                for entry in sorted(roster.entries, key=lambda x: x.variant.introduction_date):
                    entry = entry.variant.get_variants()[0]
                    if entry.techclass in ["bus", "articulated_bus", "2decker", "coach"]:
                        name = get_translation(string_manager["STR_RV_" + entry.translation_name + "_NAME"], 0x7F)
                        print(f"| {entry._props['introduction_date'].year} | {name}", file=f)

                print(
                    f"""
# Lorries

| Year  | Name |
|-------|------|""",
                    file=f,
                )
                for entry in sorted(roster.entries, key=lambda x: x.variant.introduction_date):
                    entry = entry.variant.get_variants()[0]
                    if entry.techclass in ["l_truck", "m_truck", "h_truck"]:
                        name = get_translation(string_manager["STR_RV_" + entry.translation_name + "_NAME"], 0x7F)
                        print(f"| {entry._props['introduction_date'].year} | {name}", file=f)

    prefix = f"docs/road_vehicle/vehicles"
    os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
    cc1_remap = company_colour_remap(CompanyColour.BLUE, CompanyColour.BLUE).to_sprite()
    cc2_remap = company_colour_remap(CompanyColour.WHITE, CompanyColour.RED).to_sprite()
    for i, entry in enumerate(rosters[0].entries):
        # Prepare text
        v = entry.variant
        translation = get_translation(string_manager["STR_RV_" + v["translation_name"] + "_NAME"], 0x7F)
        desc_translation = get_translation(string_manager["STR_RV_" + v["translation_name"] + "_DESC"], 0x7F)

        # Prepare graphics
        sprite = v.graphics_helper.doc_graphics()
        masked_sprite = sprite.get_sprite(zoom=grf.ZOOM_NORMAL, bpp=32)
        img, _ = masked_sprite.get_image()
        mask, _ = masked_sprite.mask.get_image()
        cc1_mask = cc1_remap.remap_image(mask)
        cc1_masked_img = blend(img, cc1_mask)
        cc1_masked_img.save(os.path.join(prefix, "img", f'{v["translation_name"]}_cc1.png'))
        cc2_mask = cc2_remap.remap_image(mask)
        cc2_masked_img = blend(img, cc2_mask)
        cc2_masked_img.save(os.path.join(prefix, "img", f'{v["translation_name"]}_cc2.png'))

        # Dump template
        with open(os.path.join(prefix, f'{v["translation_name"]}.md'), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: Vehicles
grand_parent: ACRVS - Ahyangyi's Chinese Road Vehicle Set
nav_order: {i+1}
---

{{% translate_file road_vehicle/vehicles/{v["translation_name"]}.md %}}
""",
                file=f,
            )

        # Dump
        for language in ["en-GB", "zh-CN"]:
            langprefix = f"docs/_i18n/{language}/road_vehicle/vehicles"
            INTRODUCTION = {"en-GB": "Introduction", "zh-CN": "介绍"}[language]
            DATASHEET = {"en-GB": "Datasheet", "zh-CN": "数据"}[language]

            with open(os.path.join(langprefix, f'{v["translation_name"]}.md'), "w") as f:
                print(
                    f"""
# {INTRODUCTION}
![](img/{v["translation_name"]}_cc1.png)
![](img/{v["translation_name"]}_cc2.png)
{desc_translation}

# {DATASHEET}
""",
                    file=f,
                )
