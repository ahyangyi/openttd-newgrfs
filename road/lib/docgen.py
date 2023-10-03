import os
from agrf.strings import get_translation


def gen_docs(string_manager, road_types):
    prefix = "docs/road/"
    for i, road_type in enumerate(road_types):
        translation = get_translation(string_manager[f"STR_RT_{road_type.translation_name}_NAME"], 0x7F)
        with open(os.path.join(prefix, f"{road_type.translation_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: Ahyangyi's Chinese Road Set (ACRS)
nav_order: {i+1}
---
Blablabla
""",
                file=f,
            )
