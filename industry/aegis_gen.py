#!/usr/bin/env python
import grf
import struct
import argparse
from industry.economies import vanilla_temperate, vanilla_subarctic, vanilla_subtropical, firs_arctic
from industry.lib.parameters import iterate_variations
from industry.lib.validator import validate


all_economies = [vanilla_temperate, vanilla_subarctic, vanilla_subtropical, firs_arctic]
all_industries = []
all_cargos = []
# FIXME: need to collect industry/cargo information in better ways
for meta_economy in all_economies:
    for variation in iterate_variations():
        economy = meta_economy.get_economy(variation)
        for industry in economy.industries:
            if industry not in all_industries:
                all_industries.append(industry)
        for cargo in economy.cargos:
            if cargo not in all_cargos:
                all_cargos.append(cargo)


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

    g.add(grf.DefineMultiple(feature=grf.INDUSTRY, first_id=0, props={"substitute_type": [0xFF] * 0x25}))

    # Parameter 0
    g.add_int_parameter(
        name=s["STR_PARAM_ECONOMY"],
        description=s["STR_PARAM_ECONOMY_DESC"],
        default=0,
        limits=(0, 6),
        enum={
            0: s["STR_PARAM_ECONOMY_VANILLA_TEMPERATE"],
            1: s["STR_PARAM_ECONOMY_VANILLA_SUBARCTIC"],
            2: s["STR_PARAM_ECONOMY_VANILLA_SUBTROPICAL"],
            3: s["STR_PARAM_ECONOMY_TOYLAND"],
            4: s["STR_PARAM_ECONOMY_BASIC_TEMPERATE"],
            5: s["STR_PARAM_ECONOMY_BASIC_SUBARCTIC"],
            6: s["STR_PARAM_ECONOMY_BASIC_SUBTROPICAL"],
        },
    )

    # Parameter 1
    g.add_int_parameter(
        name=s["STR_PARAM_PRESET"],
        description=s["STR_PARAM_PRESET_DESC"],
        default=0,
        limits=(0, 6),
        enum={
            0: s["STR_PARAM_PRESET_AEGIS"],
            1: s["STR_PARAM_PRESET_VANILLA"],
            2: s["STR_PARAM_PRESET_FIRS"],
            3: s["STR_PARAM_PRESET_YETI"],
            4: s["STR_PARAM_PRESET_CARIBBEAN"],
            5: s["STR_PARAM_PRESET_LUMBERJACK"],
            6: s["STR_PARAM_PRESET_ITI"],
        },
    )

    # Parameter 2
    g.add_int_parameter(
        name=s["STR_PARAM_POLICY"],
        description=s["STR_PARAM_POLICY_DESC"],
        default=0,
        limits=(0, 4),
        enum={
            0: s["STR_PARAM_POLICY_PRESET"],
            1: s["STR_PARAM_POLICY_AUTARKY"],
            2: s["STR_PARAM_POLICY_SELF_SUFFICIENT"],
            3: s["STR_PARAM_POLICY_FREE_TRADE"],
            4: s["STR_PARAM_POLICY_EXPORT"],
        },
    )

    # Parameter 3
    g.add_int_parameter(
        name=s["STR_PARAM_PAYMENT"],
        description=s["STR_PARAM_PAYMENT_DESC"],
        default=0,
        limits=(0, 2),
        enum={
            0: s["STR_PARAM_PAYMENT_PRESET"],
            1: s["STR_PARAM_PAYMENT_LINEAR"],
            2: s["STR_PARAM_PAYMENT_CONSTANT"],
        },
    )

    # Parameter 4
    g.add_int_parameter(
        name=s["STR_PARAM_WORKER"],
        description=s["STR_PARAM_WORKER_DESC"],
        default=0,
        limits=(0, 3),
        enum={
            0: s["STR_PARAM_WORKER_PRESET"],
            1: s["STR_PARAM_WORKER_NONE"],
            2: s["STR_PARAM_WORKER_PASSENGER"],
            3: s["STR_PARAM_WORKER_CENTER"],
        },
    )

    # Parameter 5
    g.add_int_parameter(
        name=s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH"],
        description=s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_DESC"],
        default=0,
        limits=(0, 7),
        enum={
            0: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_PRESET"],
            1: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_NONE"],
            2: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_GENERIC_SUPPLIES"],
            3: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_SPECIFIC_SUPPLIES"],
            4: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_TOWN_POPULATION"],
            5: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_WORKERS"],
            6: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_DISCRETE"],
            7: s["STR_PARAM_PRIMARY_INDUSTRY_GROWTH_CONTINUOUS"],
        },
    )

    # Parameter 6
    g.add_int_parameter(
        name=s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE"],
        description=s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE_DESC"],
        default=0,
        limits=(0, 3),
        enum={
            0: s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE_PRESET"],
            1: s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE_DISABLED"],
            2: s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE_ENABLED"],
            3: s["STR_PARAM_PRIMARY_INDUSTRY_CLOSURE_RESERVE"],
        },
    )

    # Parameter 7
    g.add_int_parameter(
        name=s["STR_PARAM_PRIMARY_INDUSTRY_ZONING"],
        description=s["STR_PARAM_PRIMARY_INDUSTRY_ZONING_DESC"],
        default=0,
        limits=(0, 2),
        enum={
            0: s["STR_PARAM_PRIMARY_INDUSTRY_ZONING_PRESET"],
            1: s["STR_PARAM_PRIMARY_INDUSTRY_ZONING_DISABLED"],
            2: s["STR_PARAM_PRIMARY_INDUSTRY_ZONING_ENABLED"],
        },
    )

    # Parameter 8
    g.add_int_parameter(
        name=s["STR_PARAM_SECONDARY_INDUSTRY_PROCESSING"],
        description=s["STR_PARAM_SECONDARY_INDUSTRY_PROCESSING_DESC"],
        default=0,
        limits=(0, 2),
        enum={
            0: s["STR_PARAM_SECONDARY_INDUSTRY_PROCESSING_PRESET"],
            1: s["STR_PARAM_SECONDARY_INDUSTRY_PROCESSING_STRICT"],
            2: s["STR_PARAM_SECONDARY_INDUSTRY_PROCESSING_NORMAL"],
        },
    )

    # Parameter 9
    g.add_int_parameter(
        name=s["STR_PARAM_INDUSTRY_SIZE"],
        description=s["STR_PARAM_INDUSTRY_SIZE_DESC"],
        default=2,
        limits=(0, 6),
        enum={
            0: s["STR_PARAM_INDUSTRY_SIZE_EXTRA_LARGE"],
            1: s["STR_PARAM_INDUSTRY_SIZE_LARGE"],
            2: s["STR_PARAM_INDUSTRY_SIZE_REGULAR"],
            3: s["STR_PARAM_INDUSTRY_SIZE_SMALL"],
            4: s["STR_PARAM_INDUSTRY_SIZE_TINY"],
            5: s["STR_PARAM_INDUSTRY_SIZE_ONE_TILE"],
            6: s["STR_PARAM_INDUSTRY_SIZE_ONE_TILE_FLAT"],
        },
    )

    # Parameter 10
    g.add_int_parameter(
        name=s["STR_PARAM_COLOUR_SCHEME"],
        description=s["STR_PARAM_COLOUR_SCHEME_DESC"],
        default=0,
        limits=(0, 8),
        enum={
            0: s["STR_PARAM_COLOUR_SCHEME_TWO"],
            1: s["STR_PARAM_COLOUR_SCHEME_ONE"],
            2: s["STR_PARAM_COLOUR_SCHEME_FIRS_3"],
            3: s["STR_PARAM_COLOUR_SCHEME_FIRS_4"],
            4: s["STR_PARAM_COLOUR_SCHEME_TWO_PER_INDUSTRY"],
            5: s["STR_PARAM_COLOUR_SCHEME_ONE_PER_INDUSTRY"],
            6: s["STR_PARAM_COLOUR_SCHEME_TWO_GLOBAL"],
            7: s["STR_PARAM_COLOUR_SCHEME_ONE_GLOBAL"],
            8: s["STR_PARAM_COLOUR_SCHEME_FIXED"],
        },
    )

    # Parameter 11
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

    from industry.industry_tiles import one_tile_flat

    g.add(one_tile_flat.the_industry_tile)

    for industry in all_industries:
        g.add(industry)
    for cargo in all_cargos:
        g.add(cargo)

    g.write("aegis.grf")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    args = parser.parse_args()

    if args.cmd == "gen":
        gen()
    elif args.cmd == "test":
        for meta_economy in all_economies:
            for variation in iterate_variations():
                economy = meta_economy.get_economy(variation)
                try:
                    validate(economy)
                except AssertionError as e:
                    print(f"Economy: {meta_economy.name}")
                    for k, v in variation.items():
                        print(f"{k}: {v}")
                    raise
    else:
        string_manager = get_string_manager()

        from industry.docgen.economy import gen_economy_doc

        gen_economy_doc(all_economies, string_manager)

        from industry.docgen.industry import gen_industry_doc

        gen_industry_doc(all_industries, string_manager)

        from industry.docgen.cargo import gen_cargo_doc

        gen_cargo_doc(all_cargos, string_manager)


if __name__ == "__main__":
    main()
