#!/usr/bin/env python
import grf
import struct
import argparse
from industry.economies import (
    vanilla_temperate,
    vanilla_subarctic,
    vanilla_subtropical,
    firs_temperate,
    firs_arctic,
    firs_tropical,
)
from industry.lib.parameters import parameter_list, parameter_choices
from industry.lib.validator import validate


all_economies = [vanilla_temperate, vanilla_subarctic, vanilla_subtropical, firs_temperate, firs_arctic, firs_tropical]
all_industries = []
all_cargos = []


def initialize_metadata():
    from industry.lib.industry import SplitDefinition

    # Make up the lists
    for meta_economy in all_economies:
        for variation in parameter_choices.iterate_variations():
            economy = meta_economy.get_economy(variation)
            for industry in economy.industries:
                if industry not in all_industries:
                    all_industries.append(industry)
            for cargo in economy.cargos:
                if cargo not in all_cargos:
                    all_cargos.append(cargo)

    for industry in all_industries:
        industry._props["exists"] = SplitDefinition(
            (
                "ECONOMY",
                "POLICY",
                "PRIMARY_INDUSTRY_GROWTH",
                "WORKFORCE",
                "WORKER_PARTICIPATION",
                "SEA_INDUSTRY",
                "TOWN_GOODS",
            ),
            {},
        )
        industry._props["production_types"] = SplitDefinition(
            (
                "ECONOMY",
                "POLICY",
                "PRIMARY_INDUSTRY_GROWTH",
                "WORKFORCE",
                "WORKER_PARTICIPATION",
                "SEA_INDUSTRY",
                "TOWN_GOODS",
            ),
            {},
        )
        industry._props["acceptance_types"] = SplitDefinition(
            (
                "ECONOMY",
                "POLICY",
                "PRIMARY_INDUSTRY_GROWTH",
                "WORKFORCE",
                "WORKER_PARTICIPATION",
                "SEA_INDUSTRY",
                "TOWN_GOODS",
            ),
            {},
        )

    for cargo in all_cargos:
        cargo._props["exists"] = SplitDefinition(
            (
                "ECONOMY",
                "POLICY",
                "PRIMARY_INDUSTRY_GROWTH",
                "WORKFORCE",
                "WORKER_PARTICIPATION",
                "SEA_INDUSTRY",
                "TOWN_GOODS",
            ),
            {},
        )

    for i, meta_economy in enumerate(all_economies):
        for variation in parameter_choices.iterate_variations():
            economy = meta_economy.get_economy(variation)
            index = (parameter_list["ECONOMY"].enum[i],) + tuple(
                variation[i]
                for i in (
                    "POLICY",
                    "PRIMARY_INDUSTRY_GROWTH",
                    "WORKFORCE",
                    "WORKER_PARTICIPATION",
                    "SEA_INDUSTRY",
                    "TOWN_GOODS",
                )
            )
            for industry in all_industries:
                if industry in economy.industries:
                    industry._props["exists"].branches[index] = True
                else:
                    industry._props["exists"].branches[index] = False
            for cargo in all_cargos:
                if cargo in economy.cargos:
                    cargo._props["exists"].branches[index] = True
                else:
                    cargo._props["exists"].branches[index] = False
            for industry, flow_desc in economy.graph.items():
                industry._props["production_types"].branches[index] = flow_desc.translated_produces
                industry._props["acceptance_types"].branches[index] = flow_desc.translated_accepts


def get_string_manager():
    s = grf.StringManager()
    s.import_lang_dir("industry/lang", default_lang_file="english-uk.lng")

    return s


def gen():
    s = get_string_manager()
    g = grf.NewGRF(
        grfid=b"\xe5\xbc\x8bi",
        name=s["STR_GRF_NAME"],
        description=s["STR_GRF_DESC"],
        id_map_file="industry/id_map.json",
        strings=s,
        preferred_blitter=grf.NewGRF.BLITTER_BPP_32,
    )

    from industry.lib.cargo import cargo_table

    g.set_cargo_table(cargo_table)

    g.add(grf.DefineMultiple(feature=grf.INDUSTRY, first_id=0, props={"substitute_type": [0xFF] * 0x25}))
    g.add(grf.DefineMultiple(feature=grf.CARGO, first_id=0, props={"label": [0] * 12, "bit_number": [0xFF] * 12}))

    from industry.lib.parameters import parameter_list

    parameter_list.add(g, s)

    nightgfx_id = struct.unpack("<I", b"\xffOTN")[0]
    g.add(grf.ComputeParameters(target=0x3F, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=1))
    g.add(grf.If(is_static=False, variable=0x88, condition=0x06, value=nightgfx_id, skip=1, varsize=4))
    g.add(grf.ComputeParameters(target=0x3F, operation=0x00, if_undefined=False, source1=0xFF, source2=0xFF, value=0))

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

    initialize_metadata()
    if args.cmd == "gen":
        gen()
    elif args.cmd == "test":
        for meta_economy in all_economies:
            for variation in parameter_choices.iterate_variations():
                economy = meta_economy.get_economy(variation)
                try:
                    validate(economy)
                except AssertionError:
                    print(f"Economy: {meta_economy.translation_name}")
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
