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
            for industry, flow in entry.graph.items():
                accepts = ", ".join(
                    f"[{translate(x.label)}](/openttd-newgrfs/industry/cargos/{x.label}.html)" for x in flow.accepts
                )
                produces = ", ".join(translate(x.label) for x in flow.produces)
                print(f"| {industry.name} | {accepts} | {produces} |", file=f)
