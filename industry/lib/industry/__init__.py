import grf
from industry.lib.parameters import parameter_list
from .transcriber import transcribe
from .symmetrizer import symmetrize


class SplitDefinition:
    def __init__(self, variables, branches):
        if isinstance(variables, int):
            # Legacy format
            variables = (variables,)
            branches = {(i,): b for i, b in branches.items()}
        if isinstance(variables, str):
            idx = parameter_list.index(variables)
            p = parameter_list.parameters[idx]
            variables = (idx,)
            branches = {(next(k for k, v in p.enum.items() if v == i),): b for i, b in branches.items()}
        self.variables = variables
        self.branches = branches


VARLEN = {0: 4, 9: 7}


class AIndustry(grf.SpriteGenerator):
    def __init__(self, *, name, id=None, callbacks={}, **props):
        super().__init__()
        if "override_type" in props:
            assert id is None
            id = props["override_type"]
            if "substitute_type" not in props:
                props["substitute_type"] = id
        if "substitute_type" not in props:
            props["substitute_type"] = 0x0
        self.id = id
        self.name = name
        self._props = props
        self.callbacks = grf.make_callback_manager(grf.INDUSTRY, callbacks)

    @property
    def dynamic_prop_variables(self):
        ret = set()
        for p in self._props.values():
            if isinstance(p, SplitDefinition):
                for v in p.variables:
                    ret.add(v)
        return list(sorted(ret))

    def resolve_props(self, parameters):
        new_props = {}
        miss = False
        for k, v in self._props.items():
            while isinstance(v, SplitDefinition):
                branch_key = tuple(parameters[var] for var in v.variables)
                if branch_key in v.branches:
                    v = v.branches[branch_key]
                else:
                    miss = True
                    break
            new_props[k] = v
        if new_props.get("exists", True):
            assert not miss

            # XXX: substitute_type needs to be first
            if "substitute_type" in new_props:
                new_props = {"substitute_type": new_props["substitute_type"], **new_props}
        return new_props

    def dynamic_definitions(self, all_choices, parameters, i=0):
        if i == len(all_choices):
            resolved_props = self.resolve_props(parameters)
            exists = resolved_props.pop("exists", True)
            if exists:
                return [
                    grf.Define(
                        feature=grf.INDUSTRY,
                        id=self.id,
                        props=resolved_props,
                    )
                ]
            else:
                return []
        ret = []
        var_id = all_choices[i]
        for choice in range(VARLEN[var_id]):
            parameters[var_id] = choice
            actions = self.dynamic_definitions(all_choices, parameters, i + 1)
            if len(actions) == 0:
                continue
            ret.append(
                grf.If(is_static=True, variable=var_id, condition=0x03, value=choice, skip=len(actions), varsize=4)
            )
            ret.extend(actions)
        del parameters[var_id]
        return ret

    def get_sprites(self, g):
        name_id = g.strings.add(self.name).get_persistent_id()
        self._props["name"] = name_id
        res = self.dynamic_definitions(self.dynamic_prop_variables, {}, 0)
        if len(res) == 0:
            return []
        definition = res[-1]
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res


class ADummyIndustry(AIndustry):
    def __init__(self, *, name):
        super().__init__(id=0xFF, name=name, callbacks={})

    def get_sprites(self, g):
        return []
