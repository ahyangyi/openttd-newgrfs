import grf
from industry.lib.parameters import parameter_list
from .transcriber import transcribe
from .symmetrizer import symmetrize


def props_hash(parameters):
    ret = []
    for k, v in sorted(parameters.items()):
        if k == "layouts":
            # FIXME
            pass
        else:
            ret.append((k, v))
    return hash(tuple(ret))


class SplitDefinition:
    def __init__(self, variables, branches):
        self.variables = variables
        self.branches = branches

    def fixup(self):
        if isinstance(self.variables, int):
            # Legacy format
            self.variables = (self.variables,)
            self.branches = {(i,): b for i, b in self.branches.items()}
        elif isinstance(self.variables, str):
            idx = parameter_list.index(self.variables)
            self.variables = (idx,)
            self.branches = {(parameter_list.parameters[idx].enum_index(i),): b for i, b in self.branches.items()}
        elif isinstance(self.variables[0], str):
            self.variables = tuple(parameter_list.index(idx) for idx in self.variables)
            self.branches = {
                tuple(parameter_list.parameters[idx].enum_index(s) for idx, s in zip(self.variables, i)): b
                for i, b in self.branches.items()
            }


class AIndustry(grf.SpriteGenerator):
    def __init__(self, *, translation_name, id=None, callbacks={}, **props):
        super().__init__()
        if "override_type" in props:
            assert id is None
            id = props["override_type"]
            if "substitute_type" not in props:
                props["substitute_type"] = id
        if "substitute_type" not in props:
            props["substitute_type"] = 0x0
        self.id = id
        self.translation_name = translation_name
        self._props = props
        self.callbacks = grf.make_callback_manager(grf.INDUSTRY, callbacks)

    @property
    def dynamic_prop_variables(self):
        ret = set()
        for p in self._props.values():
            if isinstance(p, SplitDefinition):
                p.fixup()
                for v in p.variables:
                    ret.add(v)
        return list(sorted(ret))

    def resolve_props(self, parameters):
        new_props = {}
        miss = False
        for k, v in self._props.items():
            while isinstance(v, SplitDefinition):
                v.fixup()
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
                            feature=grf.INDUSTRY,
                            id=self.id,
                            props=resolved_props,
                        )
                    ]
                ], props_hash(resolved_props)
            else:
                return [], 0
        ret = []
        var_id = all_choices[i]
        sublists = []
        hashes = []
        for choice in range(len(parameter_list.parameters[var_id].enum)):
            parameters[var_id] = choice
            sublist, h = self.dynamic_definitions(all_choices, parameters, i + 1)
            sublists.append(sublist)
            hashes.append(h)
        del parameters[var_id]

        if all(hashes[0] == h for h in hashes):
            return sublists[0], hash(tuple(hashes))

        for choice in range(len(parameter_list.parameters[var_id].enum)):
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

    def get_sprites(self, g):
        self._props["name"] = g.strings[f"STR_INDUSTRY_NAME_{self.translation_name}"].get_persistent_id()
        res, _ = self.dynamic_definitions(self.dynamic_prop_variables, {}, 0)
        res = [sprite for sprite_group in res for sprite in sprite_group]
        if len(res) == 0:
            return []
        definition = res[-1]
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_INDUSTRY_NAME_{self.translation_name}"], 0x7F)


class ADummyIndustry(AIndustry):
    def __init__(self, *, translation_name):
        super().__init__(id=0xFF, translation_name=translation_name, callbacks={})

    def get_sprites(self, g):
        return []
