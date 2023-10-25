import copy


class Parameter:
    def __init__(self, name, default, enum):
        self.name = name
        self.default = default
        self.enum = enum

    def add(self, g, s):
        g.add_int_parameter(
            name=s[f"STR_PARAM_{self.name}"],
            description=s[f"STR_PARAM_{self.name}_DESC"],
            default=self.default,
            limits=(min(self.enum.keys()), max(self.enum.keys())),
            enum={k: s[f"STR_PARAM_{self.name}_{v}"] for k, v in self.enum.items()},
        )


overall_list = [
    Parameter(
        "ECONOMY",
        0,
        {
            0: "VANILLA_TEMPERATE",
            1: "VANILLA_SUBARCTIC",
            2: "VANILLA_SUBTROPICAL",
            3: "BASIC_TEMPERATE",
            4: "BASIC_SUBARCTIC",
            # ?: "TOYLAND",
            # ?: "BASIC_SUBTROPICAL",
        },
    ),
    Parameter(
        "PRESET",
        0,
        {
            0: "AEGIS",
            1: "VANILLA",
            2: "FIRS",
            3: "YETI",
            4: "CARIBBEAN",
            5: "LUMBERJACK",
            6: "ITI",
        },
    ),
    Parameter(
        "POLICY",
        0,
        {
            0: "PRESET",
            1: "AUTARKY",
            2: "SELF_SUFFICIENT",
            3: "FREE_TRADE",
            4: "EXPORT",
        },
    ),
    Parameter(
        "PAYMENT",
        0,
        {
            0: "PRESET",
            1: "LINEAR",
            2: "CONSTANT",
        },
    ),
    # FIXME
    Parameter(
        "WORKER",
        0,
        {
            0: "PRESET",
            1: "NONE",
            2: "PASSENGER",
            3: "CENTER",
        },
    ),
    Parameter(
        "PRIMARY_INDUSTRY_GROWTH",
        0,
        {
            0: "PRESET",
            1: "NONE",
            2: "GENERIC_SUPPLIES",
            3: "SPECIFIC_SUPPLIES",
            4: "TOWN_POPULATION",
            5: "WORKERS",
            6: "DISCRETE",
            7: "CONTINUOUS",
        },
    ),
    Parameter(
        "PRIMARY_INDUSTRY_CLOSURE",
        0,
        {
            0: "PRESET",
            1: "DISABLED",
            2: "ENABLED",
            3: "RESERVE",
        },
    ),
    Parameter(
        "PRIMARY_INDUSTRY_ZONING",
        0,
        {
            0: "PRESET",
            1: "DISABLED",
            2: "ENABLED",
        },
    ),
    Parameter(
        "SECONDARY_INDUSTRY_PROCESSING",
        0,
        {
            0: "PRESET",
            1: "STRICT",
            2: "NORMAL",
        },
    ),
    Parameter(
        "INDUSTRY_SIZE",
        3,
        {
            0: "ENORMOUS",
            1: "HUGE",
            2: "LARGE",
            3: "REGULAR",
            4: "SMALL",
            5: "TINY",
            6: "ONE_TILE",
            7: "ONE_TILE_FLAT",
        },
    ),
    Parameter(
        "COLOUR_SCHEME",
        0,
        {
            0: "ONE",
            1: "TWO",
            2: "FIRS_3",
            3: "FIRS_4",
            4: "TWO_PER_INDUSTRY",
            5: "ONE_PER_INDUSTRY",
            6: "TWO_GLOBAL",
            7: "ONE_GLOBAL",
            8: "FIXED",
        },
    ),
    Parameter(
        "NIGHT_MODE",
        0,
        {
            0: "AUTO_DETECT",
            1: "ENABLED",
            2: "DISABLED",
        },
    ),
]

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


def fix_docs_params(cat, options):
    [(idx, all_options)] = [
        (i, the_options) for i, (the_cat, the_options) in enumerate(docs_parameter_choices) if the_cat == cat
    ]
    assert all(o in all_options for o in options)
    docs_parameter_choices[idx] = (cat, options)


fix_docs_params("WORKER", ["NONE", "PASSENGERS", "YETI"])
fix_docs_params("LAND_PORTS", ["ORGANIC"])
fix_docs_params("TOWN_GOODS", ["ORGANIC"])

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
