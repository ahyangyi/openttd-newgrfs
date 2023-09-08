#!/usr/bin/env python
import grf
import argparse


def main():
    s = grf.StringManager()
    s.import_lang_dir("road/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Br",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="road/id_map.json",
        sprite_cache_path="road/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )
    from road.road_types import slate_block, main_asphalt, motorway

    g.add(slate_block.the_road)
    g.add(main_asphalt.the_road)
    g.add(motorway.the_road)

    g.write("road.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        main()
    else:
        print("Hello, world!")


if __name__ == "__main__":
    main()
