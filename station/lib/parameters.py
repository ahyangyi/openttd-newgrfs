from agrf.parameters import Parameter, ParameterList


parameter_list = ParameterList(
    [
        Parameter("INTRODUCTION_YEAR", 0, {0: "DISABLED", 1: "ENABLED"}),
        Parameter("NIGHT_MODE", 0, {0: "AUTO_DETECT", 1: "ENABLED", 2: "DISABLED"}),
        Parameter("E88A9CA_INTRODUCTION_YEAR", 2005, limits=(0, 9999)),
    ]
)
