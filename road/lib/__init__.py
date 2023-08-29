import grf


class ARoadType(grf.SpriteGenerator):
    def __init__(self, *, id, name, sprites, toolbar_caption=None, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.name = name
        self.sprites = sprites
        self.toolbar_caption = toolbar_caption
        self.callbacks = grf.make_callback_manager(grf.ROADTYPE, callbacks)
        self._props = props

    def get_sprites(self, g):
        if self.toolbar_caption and "toolbar_caption" not in self._props:
            self._props["toolbar_caption"] = g.strings.add(self.toolbar_caption).get_persistent_id(grf.ROADTYPE)

        res = []

        if self.sprites:
            layouts = []
            for i, sprite in enumerate(self.sprites):
                layouts.append(
                    grf.GenericSpriteLayout(
                        ent1=(i,),
                        ent2=(i,),
                        feature=grf.ROADTYPE,
                    )
                )
            self.callbacks.graphics = layouts[0]

        if isinstance(self.name, grf.StringRef):
            name_action = self.name.get_actions(grf.ROADTYPE, self.id)
        else:
            name_action = g.strings.add(self.name).get_actions(grf.ROADTYPE, self.id)
        res.extend(name_action)
        res.append(definition := grf.Define(feature=grf.ROADTYPE, id=self.id, props={**self._props}))
        if self.sprites:
            res.append(
                grf.Action1(
                    feature=grf.ROADTYPE,
                    set_count=len(self.sprites),
                    sprite_count=19,
                )
            )

            for s in self.sprites:
                res.append(s)

        res.append(self.callbacks.make_map_action(definition))

        return res
