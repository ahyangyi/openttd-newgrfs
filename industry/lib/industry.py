import grf


class AIndustry(grf.SpriteGenerator):
    def __init__(self, *, name, id=None, callbacks={}, **props):
        super().__init__()
        if "substitute_type" in props:
            assert id is None
            id = props["substitute_type"]
        self.id = id
        self.name = name
        self._props = props
        self.callbacks = grf.make_callback_manager(grf.INDUSTRY, callbacks)

    def get_sprites(self, g):
        res = []
        name_id = g.strings.add(self.name).get_persistent_id()
        res.append(definition := grf.Define(feature=grf.INDUSTRY, id=self.id, props={**self._props, "name": name_id}))
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res


class ADummyIndustry(AIndustry):
    def __init__(self, *, name):
        super().__init__(id=0xFF, name=name, callbacks={})

    def get_sprites(self, g):
        return []
