#!/usr/bin/env python
import grf
from house.houses import dovemere_gable


houses = [dovemere_gable]


def main():
    s = grf.StringManager()
    s.import_lang_dir("house/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bh",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="house/id_map.json",
        sprite_cache_path="house/.cache",
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


if __name__ == "__main__":
    main()
