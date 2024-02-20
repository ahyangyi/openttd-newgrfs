import grf
from industry.lib.parameters import parameter_list
from .transcriber import transcribe, OldIndustryTileID, NewIndustryTileID
from .symmetrizer import symmetrize
from agrf.strings import get_translation
from agrf.split_action import SplitDefinition, MetaSpriteMixin


def props_hash(parameters):
    ret = []
    for k, v in sorted(parameters.items()):
        if k == "layouts":
            # FIXME
            ret.append((k, id(v)))
        else:
            ret.append((k, v))
    return hash(tuple(ret))


class AIndustry(grf.SpriteGenerator, MetaSpriteMixin):
    def __init__(self, *, translation_name, id=None, callbacks={}, **props):
        MetaSpriteMixin.__init__(self, grf.INDUSTRY, props_hash, parameter_list)
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

    def postprocess_props(self, props):
        return {"substitute_type": props["substitute_type"], **props}

    def get_sprites(self, g):
        self._props["name"] = g.strings[f"STR_INDUSTRY_NAME_{self.translation_name}"].get_persistent_id()
        res = self.dynamic_definitions()
        res = [sprite for sprite_group in res for sprite in sprite_group]
        if len(res) == 0:
            return []
        definition = res[-1]
        self.callbacks.graphics = 0
        res.extend(self.callbacks.make_map_action(definition))

        return res

    def name(self, string_manager, lang_id=0x7F):
        return get_translation(string_manager[f"STR_INDUSTRY_NAME_{self.translation_name}"], 0x7F)


class ADummyIndustry(AIndustry):
    def __init__(self, *, translation_name):
        super().__init__(id=0xFF, translation_name=translation_name, callbacks={})

    def get_sprites(self, g):
        return []
