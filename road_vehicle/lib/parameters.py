from agrf.parameters import Parameter, ParameterList


parameter_list = ParameterList(
    [
        Parameter(
            "VANILLA_RV",
            0,
            {
                0: "DISABLED",
                1: "ENABLED",
            },
        ),
        Parameter("NIGHT_MODE", 0, {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"}),
        # FIXME: change the order after migrating the code
        Parameter(
            "ROSTER",
            0,
            {
                0: "ALL",
                1: "DOVEMERE",
                2: "NORBURY",
            },
        ),
        Parameter(
            "EARLY_IMPORTED_VEHICLES",
            2,
            {
                0: "DISABLED",
                1: "ENABLED_CHEAP",
                2: "ENABLED",
                3: "ENABLED_COSTLY",
            },
        ),
        Parameter(
            "FANTASY_FREIGHT_TRAMS",
            0,
            {
                0: "DISABLED",
                1: "ENABLED",
            },
        ),
        Parameter(
            "BUS_CAPACITY",
            1,
            {
                0: "LOW",
                1: "STANDARD",
                2: "CRAMMED",
            },
        ),
        Parameter(
            "BUS_SPEED_REGULATION",
            0,
            {
                0: "DISABLED",
                1: "ENABLED",
            },
        ),
        Parameter(
            "MONORAIL",
            0,
            {
                0: "TRAIN",
                1: "TRAM",
                2: "BOTH",
                3: "NEITHER",
            },
        ),
        Parameter(
            "MONORAIL_INFRA",
            1,
            {
                0: "DISABLED",
                1: "ENABLED",
            },
        ),
    ]
)
