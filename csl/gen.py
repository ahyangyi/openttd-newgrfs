#!/usr/bin/env python
import argparse
import grf


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("csl/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()

    g = grf.NewGRF(
        grfid=b"\xE5\xAD\x97\x00",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="csl/id_map.json",
        sprite_cache_path="gcsl/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    g.write("csl.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        from grfobject.lib.docgen import gen_docs

        gen_docs(get_string_manager(), grfobjects)


if __name__ == "__main__":
    main()
