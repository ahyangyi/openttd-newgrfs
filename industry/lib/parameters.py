import copy

parameter_choices = [
    ("POLICY", ["AUTARKY", "SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"]),
    ("BOOSTER", ["NONE", "UNIVERSAL", "GENERIC", "GENERIC_PASSENGERS"]),
    (
        "WORKER",
        [
            "NONE",
            "PASSENGERS",
            "YETI",
            "YETI_TIRED_WORKER",
            "YETI_PASSENGERS",
            "YETI_MAIL",
        ],
    ),
    ("LAND_PORTS", ["ORGANIC", "LAND_ONLY", "BOTH", "SEA_ONLY"]),
    ("TOWN_GOODS", ["ORGANIC", "NONE", "SUBARCTIC", "SUBTROPICAL"]),
]


docs_parameter_choices = copy.deepcopy(parameter_choices)
docs_parameter_choices[-2] = ("LAND_PORTS", ["ORGANIC"])
docs_parameter_choices[-1] = ("TOWN_GOODS", ["ORGANIC"])

PRESETS = {
    "VANILLA": {
        "POLICY": "AUTARKY",
        "BOOSTER": "NONE",
        "WORKER": "NONE",
        "LAND_PORTS": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "FIRS": {
        "POLICY": "FREE_TRADE",
        "BOOSTER": "GENERIC",
        "WORKER": "NONE",
        "LAND_PORTS": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "YETI": {
        "POLICY": "AUTARKY",
        "BOOSTER": "UNIVERSAL",
        "WORKER": "YETI",
        "LAND_PORTS": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "CARIBBEAN": {
        "POLICY": "EXPORT",
        "BOOSTER": "GENERIC",
        "WORKER": "PASSENGERS",
        "LAND_PORTS": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "LUMBERJACK": {
        "POLICY": "AUTARKY",
        "BOOSTER": "GENERIC",
        "WORKER": "PASSENGERS",
        "LAND_PORTS": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
}


def iterate_variations(i=0, params={}, parameter_choices=parameter_choices):
    if i == len(parameter_choices):
        yield params
    else:
        for j in parameter_choices[i][1]:
            new_params = params.copy()
            new_params[parameter_choices[i][0]] = j
            for variation in iterate_variations(i + 1, new_params, parameter_choices=parameter_choices):
                yield variation


def parameter_desc(params):
    return "".join(str(options.index(params[i])) for i, options in parameter_choices)
