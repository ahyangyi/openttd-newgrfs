import os
import grf
from agrf.strings import get_translation


def cargo_class(c):
    results = []
    for x in dir(grf.CargoClass):
        if x.startswith("_"):
            continue
        if getattr(grf.CargoClass, x) & c:
            results.append(x)
    return ", ".join(results)


def gen_cargo_doc(all_cargos, string_manager):
    prefix = "docs/industry/cargos"
    for i, entry in enumerate(all_cargos):
        cargo_name = get_translation(string_manager["STR_CARGO_" + entry.label], 0x7F)
        with open(os.path.join(prefix, f"{cargo_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {cargo_name}
parent: Cargos
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Datasheet
Cargo Class: {cargo_class(entry.cargo_class)}
""",
                file=f,
            )
