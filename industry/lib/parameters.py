from agrf.parameters import Parameter, ParameterList, SearchSpace


parameter_list = ParameterList(
    [
        Parameter(
            "ECONOMY",
            0,
            {
                0: "VANILLA_TEMPERATE",
                1: "VANILLA_SUBARCTIC",
                2: "VANILLA_SUBTROPICAL",
                3: "BASIC_TEMPERATE",
                4: "BASIC_ARCTIC",
                5: "BASIC_TROPICAL",
                # ?: "TOYLAND",
            },
        ),
        Parameter(
            "PRESET", 0, {0: "AEGIS", 1: "VANILLA", 2: "FIRS", 3: "YETI", 4: "CARIBBEAN", 5: "LUMBERJACK", 6: "ITI"}
        ),
        Parameter("POLICY", 0, {0: "PRESET", 1: "AUTARKY", 2: "SELF_SUFFICIENT", 3: "FREE_TRADE", 4: "EXPORT"}),
        Parameter("PAYMENT", 0, {0: "PRESET", 1: "LINEAR", 2: "CONSTANT"}),
        Parameter(
            "WORKFORCE",
            0,
            {
                0: "PRESET",
                1: "ABSTRACT",
                2: "PROFESSIONAL",
                3: "PROFESSIONAL_PASSENGERS",
                4: "PROFESSIONAL_MAIL",
                5: "PROFESSIONAL_TIRED",
                6: "YETI",
                7: "YETI_PASSENGERS",
                8: "YETI_MAIL",
                9: "YETI_TIRED",
            },
        ),
        Parameter(
            "WORKER_PARTICIPATION",
            0,
            {0: "PRESET", 1: "NONE", 2: "PRIMARY_INDUSTRY", 3: "SECONDARY_INDUSTRY", 4: "BOTH"},
        ),
        Parameter("TOWN_GOODS", 0, {0: "PRESET", 1: "ORGANIC", 2: "NONE", 3: "FOOD", 4: "FOOD_AND_WATER"}),
        Parameter(
            "PRIMARY_INDUSTRY_GROWTH",
            0,
            {
                0: "PRESET",
                1: "NONE",
                2: "UNIVERSAL_SUPPLIES",
                3: "GENERIC_SUPPLIES",
                4: "SPECIFIC_SUPPLIES",
                7: "DISCRETE",
                8: "CONTINUOUS",
            },
        ),
        Parameter("PRIMARY_INDUSTRY_CLOSURE", 0, {0: "PRESET", 1: "DISABLED", 2: "ENABLED", 3: "RESERVE"}),
        Parameter("PRIMARY_INDUSTRY_ZONING", 0, {0: "PRESET", 1: "DISABLED", 2: "ENABLED"}),
        Parameter("SECONDARY_INDUSTRY_PROCESSING", 0, {0: "PRESET", 1: "STRICT", 2: "NORMAL"}),
        Parameter(
            "SEA_INDUSTRY", 0, {0: "PRESET", 1: "ORGANIC", 2: "LAND_ONLY", 3: "BOTH", 4: "EITHER", 5: "SEA_ONLY"}
        ),
        Parameter(
            "INDUSTRY_SIZE",
            3,
            {
                0: "ENORMOUS",
                1: "HUGE",
                2: "LARGE",
                3: "MEDIUM",
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
        Parameter("NIGHT_MODE", 0, {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"}),
    ]
)


parameter_choices = SearchSpace(
    [
        # FIXME: handle preset
        ("POLICY", ["PRESET", "AUTARKY", "SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"]),
        (
            "PRIMARY_INDUSTRY_GROWTH",
            ["PRESET", "NONE", "UNIVERSAL_SUPPLIES", "GENERIC_SUPPLIES", "SPECIFIC_SUPPLIES", "DISCRETE", "CONTINUOUS"],
        ),
        (
            "WORKFORCE",
            [
                "PRESET",
                "ABSTRACT",
                "PROFESSIONAL",
                "PROFESSIONAL_PASSENGERS",
                "PROFESSIONAL_MAIL",
                "PROFESSIONAL_TIRED",
                "YETI",
                "YETI_PASSENGERS",
                "YETI_MAIL",
                "YETI_TIRED",
            ],
        ),
        ("WORKER_PARTICIPATION", ["PRESET", "NONE", "PRIMARY_INDUSTRY", "SECONDARY_INDUSTRY", "BOTH"]),
        ("SEA_INDUSTRY", ["PRESET", "ORGANIC", "LAND_ONLY", "BOTH", "EITHER", "SEA_ONLY"]),
        ("TOWN_GOODS", ["PRESET", "ORGANIC", "NONE", "FOOD", "FOOD_AND_WATER"]),
    ],
    parameter_list,
)

docs_parameter_choices = SearchSpace(
    [
        ("POLICY", ["AUTARKY", "SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"]),
        (
            "PRIMARY_INDUSTRY_GROWTH",
            ["NONE", "UNIVERSAL_SUPPLIES", "GENERIC_SUPPLIES", "SPECIFIC_SUPPLIES"],
        ),
        (
            "WORKFORCE",
            [
                "PRESET",
                "ABSTRACT",
                "PROFESSIONAL",
                "YETI_TIRED",
            ],
        ),
        ("WORKER_PARTICIPATION", ["NONE", "PRIMARY_INDUSTRY", "SECONDARY_INDUSTRY"]),
        ("SEA_INDUSTRY", ["ORGANIC"]),
        ("TOWN_GOODS", ["ORGANIC"]),
    ],
    parameter_list,
)


PRESETS = {
    "VANILLA": {
        "POLICY": "AUTARKY",
        "PRIMARY_INDUSTRY_GROWTH": "NONE",
        "WORKFORCE": "ABSTRACT",
        "WORKER_PARTICIPATION": "NONE",
        "SEA_INDUSTRY": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "FIRS": {
        "POLICY": "FREE_TRADE",
        "PRIMARY_INDUSTRY_GROWTH": "GENERIC_SUPPLIES",
        "WORKFORCE": "ABSTRACT",
        "WORKER_PARTICIPATION": "NONE",
        "SEA_INDUSTRY": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "YETI": {
        "POLICY": "AUTARKY",
        "PRIMARY_INDUSTRY_GROWTH": "UNIVERSAL_SUPPLIES",
        "WORKFORCE": "YETI_TIRED",
        "WORKER_PARTICIPATION": "PRIMARY_INDUSTRY",
        "SEA_INDUSTRY": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "CARIBBEAN": {
        "POLICY": "EXPORT",
        "PRIMARY_INDUSTRY_GROWTH": "GENERIC_SUPPLIES",
        "WORKFORCE": "PROFESSIONAL",
        "WORKER_PARTICIPATION": "SECONDARY_INDUSTRY",
        "SEA_INDUSTRY": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
    "LUMBERJACK": {
        "POLICY": "AUTARKY",
        "PRIMARY_INDUSTRY_GROWTH": "GENERIC_SUPPLIES",
        "WORKFORCE": "PROFESSIONAL",
        "WORKER_PARTICIPATION": "SECONDARY_INDUSTRY",
        "SEA_INDUSTRY": "ORGANIC",
        "TOWN_GOODS": "ORGANIC",
    },
}
