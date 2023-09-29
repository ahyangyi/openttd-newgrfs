parameter_choices = [
    ("POLICY", ["AUTARKY", "SELF_SUFFICIENT", "FREE_TRADE", "EXPORT"]),
    ("BOOSTER", ["NONE", "UNIVERSAL", "GENERIC", "SPECIFIC"]),
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
