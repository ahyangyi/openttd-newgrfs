#!/usr/bin/env python
import argparse
import grf
from bridge.bridges.dovemere import yangtze_i, zhongjiang


bridges = [yangtze_i, zhongjiang]


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("bridge/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()

    g = grf.NewGRF(
        grfid=b"\xe5\xbc\x8bb",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="bridge/id_map.json",
        sprite_cache_path="bridge/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    from bridge.lib.parameters import parameter_list

    parameter_list.add(g, s)

    for b in bridges:
        g.add(b)

    g.write("bridge.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        from bridge.lib.docgen import gen_docs

        gen_docs(get_string_manager(), bridges)


if __name__ == "__main__":
    main()
