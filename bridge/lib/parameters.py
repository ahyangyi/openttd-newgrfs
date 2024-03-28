from agrf.parameters import Parameter, ParameterList


parameter_list = ParameterList(
    [
        Parameter(
            "SPEED_LIMIT", 2, {0: "SEVERE", 1: "RESTRICTIVE", 2: "NORMAL", 3: "PERMISSIVE", 4: "FANTASY", 5: "NO_LIMIT"}
        ),
        Parameter("NIGHT_MODE", 0, {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"}),
    ]
)
