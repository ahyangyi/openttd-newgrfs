import os
from agrf.strings import get_translation
from agrf.graphics.palette import CompanyColour, company_colour_remap

blue_remap = company_colour_remap(CompanyColour.BLUE, CompanyColour.BLUE).to_sprite()


def gen_docs(string_manager, metastations):
    prefix = "docs/station/"
    os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
    for i, metastation in enumerate(metastations):
        metastation_label = metastation.class_label.decode()
        translation = get_translation(string_manager[f"STR_STATION_CLASS_{metastation_label}"], 0x7F)

        for i, demo in enumerate(metastation.doc_layouts):
            img = demo.doc_graphics(blue_remap)
            img.save(os.path.join(prefix, "img", f"{metastation_label}_{i}.png"))

        with open(os.path.join(prefix, f"{metastation_label}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: AWSS - Ahyangyi's Wuhu Station Set
nav_order: {i+1}
---
""",
                file=f,
            )

            for i in range(len(metastation.doc_layouts)):
                print(
                    f"![](img/{metastation_label}_{i}.png)",
                    file=f,
                )
