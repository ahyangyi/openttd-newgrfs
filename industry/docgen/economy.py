import os
from agrf.strings import get_translation
from industry.lib.parameters import (
    docs_parameter_choices,
    parameter_choices,
    PRESETS,
)


default_variation = "0" * len(parameter_choices.choices)


def gen_economy_doc(all_economies, string_manager):
    prefix = "docs/industry/economies"
    for i, meta_economy in enumerate(all_economies):
        for variation in docs_parameter_choices.iterate_variations():
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
nav_exclude: true
search_exclude: true"""
            with open(os.path.join(prefix, f"{meta_economy.name}_{variation_desc}.md"), "w") as f:
                print(
                    f"""{header}
---
# Flowchart

| Industry | Accepts | Produces |
|----------|---------|----------|""",
                    file=f,
                )
                industrylink = lambda x: f"[{x}](../industries/{x}.html)"
                cargolink = lambda x: f"[{x.name(string_manager)}](../cargos/{x.label.decode()}.html)"
                for industry, flow in economy.graph.items():
                    accepts = ", ".join(cargolink(x) for x in flow.accepts)
                    produces = ", ".join(cargolink(x) for x in flow.produces)
                    print(f"| {industrylink(industry.name)} | {accepts} | {produces} |", file=f)

                # Cargos
                print(
                    """
# Cargos

| Cargo | Class | Capacity Multiplier | Weight |
|-------|-------|---------------------|--------|""",
                    file=f,
                )
                for cargo in economy.cargos:
                    from .cargo import cargo_class

                    print(
                        f"| {cargo.name(string_manager)} | {cargo_class(cargo.cargo_class)} | {cargo.capacity_multiplier / 0x100} | {cargo.weight / 16} |",
                        file=f,
                    )

                # Links: presets & variations
                print(
                    """
# Presets
""",
                    file=f,
                )

                choices_text = []
                for preset, preset_params in PRESETS.items():
                    preset_desc = parameter_choices.desc(preset_params)
                    if preset_desc == variation_desc:
                        choices_text.append(f"{preset}")
                    else:
                        choices_text.append(f"[{preset}]({meta_economy.name}_{preset_desc}.html)")
                choices_text = " \\| ".join(choices_text)
                print(
                    f"""{choices_text}

# Variations""",
                    file=f,
                )

                for i, (param, choices) in enumerate(docs_parameter_choices.choices):
                    if len(choices) == 1:
                        continue
                    choices_text = []
                    for j, choice in enumerate(choices):
                        if variation[param] == choice:
                            choices_text.append(f"{choice}")
                        else:
                            choices_text.append(
                                f"[{choice}]({meta_economy.name}_{variation_desc[:i]}{j}{variation_desc[i+1:]}.html)"
                            )
                    print(
                        f"{param}: " + " \\| ".join(choices_text) + "\n",
                        file=f,
                    )
