parameter_choices = [
    ("POLICY", ["AUTARKY", "SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"]),
    ("BOOSTER", ["NONE", "UNIVERSAL", "GENERIC", "GENERIC_PASSENGERS"]),
    (
        "WORKER",
        [
            "NONE",
            "PASSENGER",
            "YETI",
            "YETI_TIRED_WORKER",
            "YETI_PASSENGERS",
            "YETI_MAIL",
        ],
    ),
    ("LAND_PORTS", ["ORGANIC", "LAND_ONLY", "BOTH", "SEA_ONLY"]),
    ("TOWN_GOODS", ["ORGANIC", "NONE", "SUBARCTIC", "SUBTROPICAL"]),
]


def iterate_variations(i=0, params={}):
    if i == len(parameter_choices):
        yield params
    else:
        for j in parameter_choices[i][1]:
            new_params = params.copy()
            new_params[parameter_choices[i][0]] = j
            for variation in iterate_variations(i + 1, new_params):
                yield variation
