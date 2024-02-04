import copy


class Parameter:
    def __init__(self, name, default, enum):
        self.name = name
        self.default = default
        self.enum = enum
        self.reverse_lookup = {v: k for k, v in self.enum.items()}

    def add(self, g, s):
        g.add_int_parameter(
            name=s[f"STR_PARAM_{self.name}"],
            description=s[f"STR_PARAM_{self.name}_DESC"],
            default=self.default,
            limits=self.limits,
            enum={k: s[f"STR_PARAM_{self.name}_{v}"] for k, v in self.enum.items()},
        )

    @property
    def min_value(self):
        return min(self.enum.keys())

    @property
    def max_value(self):
        return max(self.enum.keys())

    @property
    def limits(self):
        return (self.min_value, self.max_value)

    @property
    def range(self):
        return (self.min_value, self.max_value + 1)

    def set_index(self, index):
        self.index = index

    def enum_index(self, name):
        return self.reverse_lookup[name]


class ParameterList:
    def __init__(self, parameters):
        self.parameters = parameters
        for i, p in enumerate(parameters):
            p.set_index(i)

    def add(self, g, s):
        for p in self.parameters:
            p.add(g, s)

    def index(self, name):
        return [i for i, p in enumerate(self.parameters) if p.name == name][0]

    def __getitem__(self, name):
        return self.parameters[self.index(name)]


class SearchSpace:
    def __init__(self, choices, parameter_list):
        self.choices = choices
        self.parameter_list = parameter_list

    def copy(self):
        return SearchSpace(copy.deepcopy(self.choices), self.parameter_list)

    def update_params(self, cat, options):
        [(idx, all_options)] = [
            (i, the_options) for i, (the_cat, the_options) in enumerate(self.choices) if the_cat == cat
        ]
        assert all(o in all_options for o in options)
        self.choices[idx] = (cat, options)

    def iterate_variations(self, i=0, params={}):
        if i == len(self.choices):
            yield params
        else:
            parameter_name, available_choices = self.choices[i]
            for j in available_choices:
                new_params = params.copy()
                new_params[parameter_name] = j
                for variation in self.iterate_variations(i + 1, new_params):
                    yield variation

    def desc(self, params):
        return "".join(str(options.index(params[i])) for i, options in self.choices)
