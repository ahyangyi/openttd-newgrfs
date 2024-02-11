from agrf.parameters import Parameter, ParameterList, SearchSpace


parameter_list = ParameterList(
    [
        Parameter(
            "VANILLA_ROAD",
            0,
            {
                0: "DISABLED",
                1: "ENABLED",
            },
        ),
        Parameter("NIGHT_MODE", 0, {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"}),
    ]
)
