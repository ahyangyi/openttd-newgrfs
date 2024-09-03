import os
from agrf.strings import get_translation, remove_control_letters
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
parent: "CNS Addon: Wuhu"
nav_order: {i+2}
has_children: True
---
""",
                file=f,
            )

        for waypoint in [False, True]:
            with open(
                os.path.join(prefix, f"{metastation_label}_{'waypoints' if waypoint else 'building_blocks'}.md"), "w"
            ) as f:
                print(
                    f"""---
    layout: default
    title: Building Blocks
    parent: {translation}
    grand_parent: "CNS Addon: Wuhu"
    nav_order: {2 if waypoint else 1}
    ---
    """,
                    file=f,
                )

                if metastation.categories is None:
                    subsections = {None: [x for x in metastation.doc_layouts if ("waypoint" not in x.notes) ^ waypoint]}
                else:
                    subsections = {k: [] for k in metastation.categories}
                    for layout in metastation.doc_layouts:
                        if ("waypoint" not in layout.notes) ^ waypoint:
                            subsections[layout.category].append(layout)

                for sub in subsections:
                    if sub is not None and len(subsections[sub]) > 0:
                        cat_name = get_translation(
                            string_manager[f"STR_STATION_CLASS_{class_label_printable(sub)}"], 0x7F
                        )
                        if "-" in cat_name:
                            cat_name = cat_name.split("-")[-1].strip()
                        cat_name = remove_control_letters(cat_name)
                        print(f"## {cat_name}", file=f)
                    for layout in sorted(subsections[sub], key=lambda x: x.station_id):
                        img = layout.graphics(4, 32, remap=get_1cc_remap(CompanyColour.BLUE)).crop().to_pil_image()
                        if "station_id" in dir(layout):
                            idstr = f"{layout.station_id:04X}"
                        img.save(os.path.join(prefix, "img", f"{metastation_label}/tiles/{idstr}.png"))
                        print(
                            f"""
    <figure style="display:inline-block">
      <img src="img/{metastation_label}/tiles/{idstr}.png" alt="{idstr}" width="64"/>
      <figcaption style="text-align:center">{idstr}</figcaption>
    </figure>
    """,
                            file=f,
                        )

        with open(os.path.join(prefix, f"{metastation_label}_layouts.md"), "w") as f:
            print(
                f"""---
layout: default
title: Sample Layouts
parent: {translation}
grand_parent: "CNS Addon: Wuhu"
nav_order: 3
---
""",
                file=f,
            )
            for i, demo in enumerate(metastation.demos):
                img = demo.graphics(4, 32).crop().resize(1920, 1080).to_pil_image()
                img.save(os.path.join(prefix, "img", f"{metastation_label}/layouts/{i}.png"))
                print(f"## {demo.title}\n\n![](img/{metastation_label}/layouts/{i}.png)", file=f)
