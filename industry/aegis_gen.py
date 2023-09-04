#!/usr/bin/env python
import grf


def main():
    s = grf.StringManager()
    s.import_lang_dir("industry/lang", default_lang_file="english-uk.lng")

    g = grf.NewGRF(
        grfid=b"\xE5\xBC\x8Bi",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="industry/id_map.json",
        bpp=32,
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
    g.add(grf.If(is_static=True, variable=0, condition=0x02, value=1, skip=1, varsize=4))
    g.add(grf.DefineMultiple(feature=grf.RV, first_id=0, props={"climates_available": [0] * 88}))

    g.write("aegis.grf")


if __name__ == "__main__":
    main()
