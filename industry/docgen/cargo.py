import os
import grf
from agrf.graphics import LayeredImage, SCALE_TO_ZOOM


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
    os.makedirs(os.path.join(prefix, "images"), exist_ok=True)
    for i, cargo in enumerate(all_cargos):
        name = cargo.name(string_manager)
        with open(os.path.join(prefix, f"{cargo.label.decode()}.md"), "w") as f:
            if cargo.graphics:
                img = (
                    LayeredImage.from_sprite(cargo.graphics.get_sprite(zoom=SCALE_TO_ZOOM[4], bpp=32))
                    .crop()
                    .to_pil_image()
                )
                img_path = os.path.join(prefix, f"images/{name}.png")
                img.save(img_path)
                img_clause = f"""
<figure style="display:inline-block">
  <img src="{img_path}" width="40"/>
  <figcaption style="text-align:center">cargo icon</figcaption>
</figure>"""
            else:
                img_clause = ""

            print(
                f"""---
layout: default
title: {name}
parent: Cargos
grand_parent: AEGIS - Ahyangyi's Extended Generic Industry Set
nav_order: {i+1}
---
{img_clause}

# Datasheet

**Cargo Class**: {cargo_class(cargo.cargo_class)}

**Capacity Multiplier**: {cargo.capacity_multiplier / 0x100}

**Weight**: {cargo.weight / 16}

**Is a freight cargo**: {cargo._props["is_freight"]}

**Price**: {cargo.base_price} \\| {cargo.penalty1} \\| {cargo.penalty2}
""",
                file=f,
            )
