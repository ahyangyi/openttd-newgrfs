import os
import grf
from agrf.strings import get_translation


def gen_docs(string_manager, road_types):
    prefix = "docs/road/"
    os.makedirs(os.path.join(prefix, "img"), exist_ok=True)
    for i, road_type in enumerate(road_types):
        translation = get_translation(string_manager[f"STR_RT_{road_type.translation_name}_NAME"], 0x7F)
        with open(os.path.join(prefix, f"{road_type.translation_name}.md"), "w") as f:
            print(
                f"""---
layout: default
title: {translation}
parent: ACRS - Ahyangyi's Chinese Road Set
nav_order: {i+1}
---
""",
                file=f,
            )

            for layer in ["underlay", "overlay"]:
                if getattr(road_type, layer) is None:
                    continue
                img, bpp = getattr(road_type, layer)[0].get_sprite(zoom=grf.ZOOM_4X, bpp=32).sprite.get_image()
                img.save(os.path.join(prefix, "img", f"{road_type.translation_name}_{layer}.png"))
                print(f"{layer} ![](img/{road_type.translation_name}_{layer}.png)", file=f)
