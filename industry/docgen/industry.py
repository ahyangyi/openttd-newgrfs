import os


def gen_industry_doc(all_industries, string_manager):
    prefix = "docs/industry/industries"
    for i, industry in enumerate(all_industries):
        with open(os.path.join(prefix, f"{industry.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {industry.name}
parent: Industries
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Datasheet
""",
                file=f,
            )
