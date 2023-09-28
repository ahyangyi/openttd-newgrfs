parameter_choices = [
    ("POLICY", ["AUTARKY"]),
    ("BOOSTER", ["NONE", "GENERIC"]),
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
