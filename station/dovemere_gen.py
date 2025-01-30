#!/usr/bin/env python
import grf
import argparse
import struct
from station.lib.docgen import gen_docs
import station.stations.dovemere_2018
import station.stations.dovemere_1934
import station.stations.platforms
from station.lib.parameters import parameter_list
from station.lib.idmap import station_idmap

metastations = [
    station.stations.dovemere_2018.the_stations,
    station.stations.dovemere_1934.the_stations,
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
        version=18,
        min_compatible_version=14,
        id_map_file="station/id_map.json",
        sprite_cache_path="station/.cache",
        url="https://www.tt-forums.net/viewtopic.php?t=91092",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    nightgfx_id = struct.unpack("<I", b"\xffOTN")[0]
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=1))
    g.add(grf.If(is_static=False, variable=0x88, condition=0x06, value=nightgfx_id, skip=1, varsize=4))
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=0))

    parameter_list.add(g, s)
    for metastation in metastations:
        metastation.check_id_uniqueness()
        metastation.remap(station_idmap=station_idmap)
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
