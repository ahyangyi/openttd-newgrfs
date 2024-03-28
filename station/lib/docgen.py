import os
from agrf.strings import get_translation
from agrf.graphics.palette import CompanyColour, company_colour_remap

blue_remap = company_colour_remap(CompanyColour.BLUE, CompanyColour.BLUE).to_sprite()


def gen_docs(string_manager, metastations):
    prefix = "docs/station/"
    for i, metastation in enumerate(metastations):
        metastation_label = metastation.class_label_plain
        translation = get_translation(string_manager[f"STR_METASTATION_CLASS_{metastation_label}"], 0x7F)
        os.makedirs(os.path.join(prefix, "img", metastation_label, "layouts"), exist_ok=True)
        os.makedirs(os.path.join(prefix, "img", metastation_label, "tiles"), exist_ok=True)

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

            print("# Building Blocks", file=f)
            if metastation.categories is None:
                subsections = [None]
            else:
                subsections = metastation.categories
            for sub in subsections:
                if sub is not None:
                    print(f"## Category {sub}", file=f)
                for i, layout in enumerate(metastation.doc_layouts):
                    if sub is not None and layout.category != sub:
                        continue
                    # FIXME
                    from station.lib import Demo

                    demo = Demo("", [[layout]])
                    img = demo.graphics(blue_remap, 4, 32).crop().to_pil_image()
                    img.save(os.path.join(prefix, "img", f"{metastation_label}/tiles/{i}.png"))
                    print(f'![](img/{metastation_label}/tiles/{i}.png){{: width="64"}}', file=f)
            print("# Sample Layouts", file=f)
            for i, demo in enumerate(metastation.demos):
                img = demo.graphics(blue_remap, 4, 32).crop().to_pil_image()
                img.save(os.path.join(prefix, "img", f"{metastation_label}/layouts/{i}.png"))
                print(f"## {demo.title}\n\n![](img/{metastation_label}/layouts/{i}.png)", file=f)
