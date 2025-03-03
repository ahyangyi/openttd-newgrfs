#!/usr/bin/env python
import argparse
import grf
from house.houses.generic import traditional_suburban_houses


houses = [traditional_suburban_houses]


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("house/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()

    g = grf.NewGRF(
        grfid=b"\xe5\xbc\x8bh",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="house/id_map.json",
        sprite_cache_path="house/.cache",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    g.add_int_parameter(
        name=s["STR_PARAM_VANILLA"],
        description=s["STR_PARAM_VANILLA_DESC"],
        default=0,
        limits=(0, 1),
        enum={0: s["STR_PARAM_VANILLA_DISABLED"], 1: s["STR_PARAM_VANILLA_ENABLED"]},
    )
    g.add(grf.If(is_static=True, variable=0, condition=0x02, value=1, skip=1, varsize=4))
    g.add(grf.DefineMultiple(feature=grf.HOUSE, first_id=0, props={"substitute": [0xFF] * 0x6E}))

    for house in houses:
        g.add(house)

    g.write("house.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        from house.lib.docgen import gen_docs

        gen_docs(get_string_manager(), houses)


if __name__ == "__main__":
    main()
