import os
from agrf.strings import get_translation


def gen_economy_doc(all_economies, string_manager):
    prefix = "docs/industry/economies"
    for i, entry in enumerate(all_economies):
        with open(os.path.join(prefix, f"{entry.name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {entry.name}
parent: Economies
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Flowchart

| Industry | Accepts | Produces |
|----------|---------|----------|""",
                file=f,
            )
            translate = lambda x: get_translation(string_manager["STR_CARGO_" + x.decode()], 0x7F)
            for industry, (i, o) in entry.graph.items():
                accepts = ", ".join(translate(x.label) for x in i)
                produces = ", ".join(translate(x.label) for x in o)
                print(f"| {industry.name} | {accepts} | {produces} |", file=f)

            # Town industry
            accepts = ", ".join(translate(x.label) for x in entry.town_cargos if x is not None)
            produces = ", ".join(translate(x.label) for x in entry.town_cargos[:2] if x is not None)
            print(f"| Towns | {accepts} | {produces} |", file=f)
