import os


def gen_economy_doc(all_economies, string_manager):
    prefix = "docs/industry/economies"
    for i, entry in enumerate(all_economies):
        v = entry.the_economy
        with open(os.path.join(prefix, f"{v.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {v.name}
parent: Economies
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Flowchart

| Industry | Accepts | Produces |
|----------|---------|----------|""",
                file=f,
            )
            for industry, (i, o) in v.graph.items():
                accepts = ", ".join(x.name for x in i)
                produces = ", ".join(x.name for x in o)
                print(f"| {industry.name} | {accepts} | {produces} |", file=f)
