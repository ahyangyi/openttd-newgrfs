#!/usr/bin/env python
import os
import grf
import struct
import argparse
from industry.economies import vanilla_temperate, vanilla_subarctic

all_economies = [vanilla_subarctic, vanilla_temperate]
all_industries = []
for economy in all_economies:
    for industry in economy.the_economy.industries:
        all_industries.append(industry)


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("industry/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()
    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bi",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="industry/id_map.json",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    # Parameter 0
    g.add_int_parameter(
        name=s["STR_PARAM_ECONOMY"],
        description=s["STR_PARAM_ECONOMY_DESC"],
        default=0,
        limits=(0, 3),
        enum={
            0: s["STR_PARAM_ECONOMY_VANILLA_TEMPERATE"],
            1: s["STR_PARAM_ECONOMY_VANILLA_SUBARCTIC"],
            2: s["STR_PARAM_ECONOMY_VANILLA_SUBTROPICAL"],
            3: s["STR_PARAM_ECONOMY_TOYLAND"],
        },
    )

    # Parameter 1
    g.add_int_parameter(
        name=s["STR_PARAM_PRESET"],
        description=s["STR_PARAM_PRESET_DESC"],
        default=0,
        limits=(0, 4),
        enum={
            0: s["STR_PARAM_PRESET_AEGIS"],
            1: s["STR_PARAM_PRESET_VANILLA"],
            2: s["STR_PARAM_PRESET_FIRS"],
            3: s["STR_PARAM_PRESET_YETI"],
            4: s["STR_PARAM_PRESET_ITI"],
        },
    )

    # Parameter 2
    g.add_int_parameter(
        name=s["STR_PARAM_NIGHT_MODE"],
        description=s["STR_PARAM_NIGHT_MODE_DESC"],
        default=0,
        limits=(0, 2),
        enum={
            0: s["STR_PARAM_NIGHT_MODE_AUTO_DETECT"],
            1: s["STR_PARAM_NIGHT_MODE_ENABLED"],
            2: s["STR_PARAM_NIGHT_MODE_DISABLED"],
        },
    )
    nightgfx_id = struct.unpack("<I", b"\xffOTN")[0]
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=1))
    g.add(grf.If(is_static=False, variable=0x88, condition=0x06, value=nightgfx_id, skip=1, varsize=4))
    g.add(grf.ComputeParameters(target=0x41, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=0))

    for industry in all_industries:
        g.add(industry)

    g.write("aegis.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    else:
        string_manager = get_string_manager()

        prefix = "docs/industry/industries"
        for i, entry in enumerate(all_industries):
            with open(os.path.join(prefix, f"{entry.name}.md"), "w") as f:
                print(
                    f"""---
layout: default
title: {entry.name}
parent: Industries
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Datasheet
""",
                    file=f,
                )

        prefix = "docs/industry/economies"
        for i, entry in enumerate(all_economies):
            v = entry.the_economy
            with open(os.path.join(prefix, f"{v.name}.md"), "w") as f:
                print(
                    f"""---
layout: default
title: {v.name}
parent: Economies
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}
---
# Flowchart

| Industry | Accepts | Produces |
|----------|---------|----------|""",
                    file=f,
                )
                for industry in v.industries:
                    print(f"| {industry.name} | | |", file=f)


if __name__ == "__main__":
    main()
