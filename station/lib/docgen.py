import os
from agrf.strings import get_translation
from agrf.graphics.palette import CompanyColour
from .utils import get_1cc_remap, class_label_printable


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
parent: CNSPS Addon: Wuhu
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
                    cat_name = get_translation(string_manager[f"STR_STATION_CLASS_{class_label_printable(sub)}"], 0x7F)
                    if "-" in cat_name:
                        cat_name = cat_name.split("-")[-1].strip()
                    print(f"## {cat_name}", file=f)
                for i, layout in enumerate(metastation.doc_layouts):
                    if sub is not None and layout.category != sub:
                        continue
                    img = layout.graphics(4, 32, remap=get_1cc_remap(CompanyColour.BLUE)).crop().to_pil_image()
                    img.save(os.path.join(prefix, "img", f"{metastation_label}/tiles/{i}.png"))
                    print(f'![](img/{metastation_label}/tiles/{i}.png){{: width="64"}}', file=f)
            print("# Sample Layouts", file=f)
            for i, demo in enumerate(metastation.demos):
                img = demo.graphics(4, 32).crop().resize(1920, 1080).to_pil_image()
                img.save(os.path.join(prefix, "img", f"{metastation_label}/layouts/{i}.png"))
                print(f"## {demo.title}\n\n![](img/{metastation_label}/layouts/{i}.png)", file=f)
