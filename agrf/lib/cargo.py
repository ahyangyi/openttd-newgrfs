import grf


class Cargo(grf.SpriteGenerator):
    def __init__(self, id, **props):
        self.id = id
        self._props = props
        self.callbacks = grf.make_callback_manager(grf.CARGO, {})

    def get_sprites(self, g):
        extra_props = {}
        for p in [
            "type_text",
            "unit_text",
            "one_text",
            "many_text",
            "abbr_text",
        ]:
            if self._props.get(p):
                s = self._props[p]
                if isinstance(s, grf.StringRef):
                    extra_props[p] = s.get_persistent_id()
                else:
                    extra_props[p] = g.strings.add(s).get_persistent_id()

        res = []
        res.append(definition := grf.Define(feature=grf.CARGO, id=self.id, props={**self._props, **extra_props}))
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res
