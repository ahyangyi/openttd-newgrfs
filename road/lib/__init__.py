import grf


class ARoadType(grf.SpriteGenerator):
    def __init__(self, *, id, name, sprites, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.name = name
        self.sprites = sprites
        self.callbacks = grf.make_callback_manager(grf.ROADTYPE, callbacks)
        self._props = props

    def get_sprites(self, g):
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
