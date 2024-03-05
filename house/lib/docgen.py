import os


def gen_docs(string_manager, houses):
    prefix = "docs/house/"
    for i, house in enumerate(houses):
        with open(os.path.join(prefix, f"{house.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {house.name}
parent: AWHS - Ahyangyi's Wuhu House Set
nav_order: {i+1}
---
""",
                file=f,
            )
