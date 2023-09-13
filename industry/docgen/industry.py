import os


def gen_industry_doc(all_industries, string_manager):
    prefix = "docs/industry/industries"
    for i, entry in enumerate(all_industries):
        with open(os.path.join(prefix, f"{entry.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {entry.name}
parent: Industries
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Datasheet
""",
                file=f,
            )
