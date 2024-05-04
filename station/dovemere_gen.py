#!/usr/bin/env python
import grf
import argparse
from station.lib.docgen import gen_docs
import station.stations.dovemere_1992
import station.stations.dovemere_2018
import station.stations.platforms

metastations = [
    station.stations.dovemere_1992.the_stations,
    station.stations.dovemere_2018.the_stations,
    station.stations.platforms.the_stations,
]


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("station/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()
    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bs",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        version=3,
        min_compatible_version=1,
        id_map_file="station/id_map.json",
        sprite_cache_path="station/.cache",
        url="https://www.tt-forums.net/viewtopic.php?t=91092",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    for metastation in metastations:
        g.add(metastation)

    g.write("station.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        gen_docs(get_string_manager(), metastations)


if __name__ == "__main__":
    main()
