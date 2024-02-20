import copy
import grf


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

    def get_effective_enum(self, i):
        return self.parameters[i].enum


class ParameterListWithPreset(ParameterList):
    def __init__(self, parameters, presets, start_id=0x40, preset_param_name="PRESET", preset_enum_name="PRESET"):
        super().__init__(parameters)
        self.presets = presets
        self.preset_param_id = self.index(preset_param_name)
        self._parameters_with_preset = {}
        for p in self.presets.values():
            for k in p.keys():
                if k not in self._parameters_with_preset:
                    self._parameters_with_preset[k] = (
                        start_id,
                        self[k].enum_index(preset_enum_name),
                        {kk: v for kk, v in self[k].enum.items() if v != preset_enum_name},
                    )
                    start_id += 1

    def preset_index(self, name):
        return self._parameters_with_preset[name]

    def add(self, g, s):
        super().add(g, s)
        for k, (v, preset_enum_id, _) in sorted(self._parameters_with_preset.items()):
            k_id = self.index(k)
            for preset_name, preset in self.presets.items():
                preset_id = self.parameters[self.preset_param_id].enum_index(preset_name)
                g.add(
                    grf.If(
                        is_static=True,
                        variable=self.preset_param_id,
                        condition=0x02,
                        value=preset_id,
                        skip=2,
                        varsize=4,
                    )
                )
                g.add(grf.If(is_static=True, variable=v, condition=0x02, value=preset_enum_id, skip=1, varsize=4))
                g.add(
                    grf.ComputeParameters(
                        target=v,
                        operation=0x00,
                        if_undefined=False,
                        source1=self[k].enum_index(preset[k]),
                        source2=0xFF,
                        value=0,
                    )
                )

    def get_effective_enum(self, i):
        name = self.parameters[i].name
        if name in self._parameters_with_preset:
            return self._parameters_with_preset[name][2]
        return super().get_effective_enum(i)


class SearchSpace:
    def __init__(self, choices, parameter_list):
        self.choices = choices
        self.parameter_list = parameter_list

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
