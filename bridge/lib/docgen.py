import os
from agrf.strings import get_translation


def gen_docs(string_manager, bridges):
    prefix = "docs/bridge/"
    for i, bridge in enumerate(bridges):
        with open(os.path.join(prefix, f"{bridge.translation_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {bridge.name(string_manager)}
parent: AWBS - Ahyangyi's Wuhu Bridge Set
nav_order: {i+1}
---
""",
                file=f,
            )
