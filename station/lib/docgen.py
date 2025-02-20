import os
from agrf.strings import get_translation, remove_control_letters
from agrf.graphics.palette import CompanyColour
from .utils import get_1cc_remap, class_label_printable
from station.lib.idmap import station_idmap


def gen_docs(string_manager, metastations):
    prefix = "docs/station/"
    for i, metastation in enumerate(metastations):
        metastation_label = metastation.class_label_plain
        translation = get_translation(string_manager[f"STR_METASTATION_CLASS_{metastation_label}"], 0x7F)
        for kind in ["layouts", "stations", "waypoints", "road_stops", "objects"]:
            os.makedirs(os.path.join(prefix, "img", metastation_label, kind), exist_ok=True)

        with open(os.path.join(prefix, f"{metastation_label}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: "China Set: Stations - Wuhu"
nav_order: {i+2}
has_children: True
---
""",
                file=f,
            )

        for kind in ["waypoints", "stations", "road_stops", "objects"]:
            if kind == "road_stops":
                pool = [x for x in metastation.road_stops if not x.is_waypoint]
            elif kind == "objects":
                pool = metastation.objects
            else:
                pool = metastation.stations

            if metastation.categories is None:
                subsections = {
                    None: [
                        x
                        for x in pool
                        if (("waypoint" not in x.doc_layout.notes) ^ (kind == "waypoints"))
                        and "noshow" not in x.doc_layout.notes
                    ]
                }
            else:
                subsections = {k: [] for k in metastation.categories}
                for layout in pool:
                    if (
                        ("waypoint" not in layout.doc_layout.notes) ^ (kind == "waypoints")
                    ) and "noshow" not in layout.doc_layout.notes:
                        subsections[layout.doc_layout.category].append(layout)

            if all(len(v) == 0 for v in subsections.values()):
                continue

            with open(os.path.join(prefix, f"{metastation_label}_{kind}.md"), "w") as f:
                title, nav_order = {
                    "stations": ("Building Blocks", 0),
                    "waypoints": ("Waypoints", 1),
                    "road_stops": ("Road Stops", 2),
                    "objects": ("Objects", 4),
                }[kind]
                print(
                    f"""---
layout: default
title: {title}
parent: {translation}
grand_parent: "China Set: Stations - Wuhu"
nav_order: {nav_order}
---
""",
                    file=f,
                )

                for sub in subsections:
                    if sub is not None and len(subsections[sub]) > 0:
                        cat_name = get_translation(
                            string_manager[f"STR_STATION_CLASS_{class_label_printable(sub)}"], 0x7F
                        )
                        if "-" in cat_name:
                            cat_name = cat_name.split("-")[-1].strip()
                        cat_name = remove_control_letters(cat_name)
                        print(f"## {cat_name}", file=f)
                    for layout in sorted(subsections[sub], key=lambda x: x.id):
                        img = (
                            layout.doc_layout.graphics(4, 32, remap=get_1cc_remap(CompanyColour.BLUE))
                            .crop()
                            .to_pil_image()
                        )
                        idstr = f"{layout.id:04X}"
                        idpath = idstr
                        if kind in ["waypoints", "stations"] and layout.id in station_idmap:
                            idstr += f" ({station_idmap[layout.id]:04X})"
                        img.save(os.path.join(prefix, "img", f"{metastation_label}/{kind}/{idpath}.png"))
                        print(
                            f"""
<figure style="display:inline-block">
  <img src="img/{metastation_label}/{kind}/{idpath}.png" width="64"/>
  <figcaption style="text-align:center">{idstr}</figcaption>
</figure>
""",
                            file=f,
                        )

        for demoi, (demok, demov) in enumerate(metastation.demos.items()):
            os.makedirs(os.path.join(prefix, "img", metastation_label, "layouts", demok), exist_ok=True)
            with open(os.path.join(prefix, f"{metastation_label}_{demok}.md"), "w") as f:
                print(
                    f"""---
layout: default
title: {demok}
parent: {translation}
grand_parent: "China Set: Stations - Wuhu"
nav_order: {5+demoi}
---
""",
                    file=f,
                )
                for i, demo in enumerate(demov):
                    img = demo.graphics(4, 32).crop().resize(1920, 1080).to_pil_image()
                    img.save(os.path.join(prefix, "img", f"{metastation_label}/layouts/{demok}/{i:04X}.png"))
                    print(f"## {demo.title}\n\n![](img/{metastation_label}/layouts/{demok}/{i:04X}.png)", file=f)
