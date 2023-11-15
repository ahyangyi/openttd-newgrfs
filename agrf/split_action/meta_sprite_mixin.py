import grf
from .split_definition import SplitDefinition


class MetaSpriteMixin:
    # FIXME: handle make this an actual mixin
    def __init__(self, feature, props_hash, parameter_list, priority_props=()):
        self.feature = feature
        self.props_hash = props_hash
        self._parameter_list = parameter_list
        self._priority_props = priority_props

    @property
    def dynamic_prop_variables(self):
        ret = set()
        for p in self._props.values():
            if isinstance(p, SplitDefinition):
                p.fixup(self._parameter_list)
                for v in p.variables:
                    ret.add(v)
        return list(sorted(ret))

    def resolve_props(self, parameters):
        new_props = {}
        miss = False
        for k, v in self._props.items():
            while isinstance(v, SplitDefinition):
                v.fixup(self._parameter_list)
                branch_key = tuple(parameters[var] for var in v.variables)
                if branch_key in v.branches:
                    v = v.branches[branch_key]
                else:
                    miss = True
                    break
            new_props[k] = v
        if new_props.get("exists", True):
            assert not miss
            new_props = {**{p: new_props[p] for p in self._priority_props if p in new_props}, **new_props}
        else:
            new_props = {"exists": False}
        return new_props

    def dynamic_definitions(self, all_choices, parameters, i=0):
        if i == len(all_choices):
            resolved_props = self.resolve_props(parameters)
            exists = resolved_props.pop("exists", True)
            if exists:
                return [
                    [
                        grf.Define(
                            feature=self.feature,
                            id=self.id,
                            props=resolved_props,
                        )
                    ]
                ], self.props_hash(resolved_props)
            else:
                return [], 0
        ret = []
        var_id = all_choices[i]
        sublists = []
        hashes = []
        for choice in range(len(self._parameter_list.parameters[var_id].enum)):
            parameters[var_id] = choice
            sublist, h = self.dynamic_definitions(all_choices, parameters, i + 1)
            sublists.append(sublist)
            hashes.append(h)
        del parameters[var_id]

        if all(hashes[0] == h for h in hashes):
            return sublists[0], hash(tuple(hashes))

        for choice in range(len(self._parameter_list.parameters[var_id].enum)):
            sublist = sublists[choice]
            for g in sublist:
                ret.append(
                    [grf.If(is_static=True, variable=var_id, condition=0x03, value=choice, skip=len(g), varsize=4)] + g
                )

        compressed_ret = []
        cur_group = []
        for group in ret:
            if len(cur_group) + len(group) + i <= 255:
                cur_group.extend(group)
            else:
                compressed_ret.append(cur_group)
                cur_group = group
        if len(cur_group) > 0:
            compressed_ret.append(cur_group)

        return compressed_ret, hash(tuple(hashes))
