#!/usr/bin/env python
import grf
import argparse
from road.road_types import slate_block, main_asphalt, motorway
from road.tram_types import monorail

road_types = [slate_block, main_asphalt, motorway, monorail]


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

    from road.lib.parameters import parameter_list
    parameter_list.add(g, s)

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
        from road.lib.docgen import gen_docs

        gen_docs(get_string_manager(), road_types)


if __name__ == "__main__":
    main()
