#!/usr/bin/env python
import grf
import argparse
import os
from road.road_types import slate_block, main_asphalt, motorway

road_types = [slate_block, main_asphalt, motorway]


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("road/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Br",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="road/id_map.json",
        sprite_cache_path="road/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    for road_type in road_types:
        g.add(road_type)

    g.write("road.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        string_manager = get_string_manager()
        prefix = "docs/road/"
        for i, road_type in enumerate(road_types):
            translated_names = string_manager["STR_RT_" + road_type.translation_name + "_NAME"].get_pairs()
            [translation] = [s.decode() for (lang_id, s) in translated_names if lang_id == 0x7F]
            with open(os.path.join(prefix, f"{road_type.translation_name}.md"), "w") as f:
                print(
                    f"""---
layout: default
title: {translation}
parent: Ahyangyi's Chinese Road Set (ACRS)
nav_order: {i+1}
---
Blablabla
""",
                    file=f,
                )


if __name__ == "__main__":
    main()
