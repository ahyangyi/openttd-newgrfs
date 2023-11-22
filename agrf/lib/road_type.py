import grf


class RoadType(grf.SpriteGenerator):
    def __init__(self, *, id, underlay, **props):
        super().__init__()
        self.id = id
        self.underlay = underlay
        self._props = props

    def get_sprites(self, g):
        extra_props = {}
        for p in [
            "toolbar_caption",
            "menu_text",
            "build_window_caption",
            "autoreplace_text",
            "new_engine_text",
            "name",
        ]:
            if self._props.get(p):
                s = self._props[p]
                if isinstance(s, grf.StringRef):
                    extra_props[p] = s.get_persistent_id()
                else:
                    extra_props[p] = g.strings.add(s).get_persistent_id()

        res = []

        if self.underlay:
            layouts = []
            for i, sprite in enumerate(self.underlay):
                layouts.append(grf.GenericSpriteLayout(ent1=(i,), ent2=(i,), feature=grf.ROADTYPE))

        res.append(definition := grf.Define(feature=grf.ROADTYPE, id=self.id, props={**self._props, **extra_props}))
        if self.underlay:
            res.append(grf.Action1(feature=grf.ROADTYPE, set_count=1, sprite_count=19))

            for s in self.underlay:
                res.append(s)

        res.append(grf.Map(definition=definition, maps={0x02: layouts[0]}, default=layouts[0]))

        return res
