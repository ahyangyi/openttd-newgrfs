import os
from agrf.strings import get_translation
from industry.lib.parameters import parameter_choices, iterate_variations


default_variation = "0" * len(parameter_choices)


def gen_economy_doc(all_economies, string_manager):
    prefix = "docs/industry/economies"
    for i, meta_economy in enumerate(all_economies):
        for variation in iterate_variations():
            economy = meta_economy.get_economy(variation)
            variation_desc = economy.parameter_desc
            if variation_desc == default_variation:
                header = f"""---
layout: default
title: {meta_economy.name}
parent: Economies
grand_parent: Ahyangyi's Extended Generic Industry Set (AEGIS)
nav_order: {i+1}"""
            else:
                header = f"""---
layout: default
title: {meta_economy.name}
nav_exclude: true"""
            with open(os.path.join(prefix, f"{meta_economy.name}_{variation_desc}.md"), "w") as f:
                print(
                    f"""{header}
---
# Flowchart

| Industry | Accepts | Produces |
|----------|---------|----------|""",
                    file=f,
                )
                translate = lambda x: get_translation(string_manager["STR_CARGO_" + x.decode()], 0x7F)
                industrylink = lambda x: f"[{translate(x.label)}](../industries/{x}.html)"
                cargolink = lambda x: f"[{translate(x.label)}](../cargos/{x.label.decode()}.html)"
                for industry, flow in economy.graph.items():
                    accepts = ", ".join(cargolink(x) for x in flow.accepts)
                    produces = ", ".join(cargolink(x) for x in flow.produces)
                    print(f"| {industrylink(industry.name)} | {accepts} | {produces} |", file=f)
                print(
                    """
# Variations
""",
                    file=f,
                )
                for i, (param, choices) in enumerate(parameter_choices):
                    choices_text = []
                    for j, choice in enumerate(choices):
                        if variation[param] == choice:
                            choices_text.append(f"{choice}")
                        else:
                            choices_text.append(
                                f"[{choice}]({meta_economy.name}_{variation_desc[:i]}{j}{variation_desc[i+1:]}.html)"
                            )
                    print(
                        f"{param}: " + " \| ".join(choices_text) + "\n",
                        file=f,
                    )
