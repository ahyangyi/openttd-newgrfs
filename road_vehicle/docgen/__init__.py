import os
import grf
from agrf.strings import get_translation
from agrf.graphics.blend import blend
from agrf.graphics.palette import CompanyColour, company_colour_remap


def gen_docs(string_manager, rosters):
    prefix = "docs/road_vehicle/rosters"
    for i, roster in enumerate(rosters):
        with open(os.path.join(prefix, f"{roster.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {roster.name}
parent: Rosters
grand_parent: Ahyangyi's Road Vehicles (ARV)
nav_order: {i+1}
---
""",
                file=f,
            )

    prefix = "docs/road_vehicle/vehicles"
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
