import os
import grf


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
    for i, cargo in enumerate(all_cargos):
        with open(os.path.join(prefix, f"{cargo.label.decode()}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {cargo.name(string_manager)}
parent: Cargos
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Datasheet
**Cargo Class**: {cargo_class(cargo.cargo_class)}

**Capacity Multiplier**: {cargo.capacity_multiplier / 0x100}

**Weight**: {cargo.weight / 16}
""",
                file=f,
            )
