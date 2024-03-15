import os
import grf
from agrf.strings import get_translation


def gen_docs(string_manager, metastations):
    prefix = "docs/station/"
    os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
    for i, metastation in enumerate(metastations):
        translation = get_translation(string_manager[f"STR_STATION_CLASS_{metastation.class_label.decode()}"], 0x7F)
        with open(os.path.join(prefix, f"{metastation.class_label.decode()}.md"), "w") as f:
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
