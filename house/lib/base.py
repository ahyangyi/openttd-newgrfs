import grf


class AHouse(grf.SpriteGenerator):
    def __init__(self, *, id, name, sprites, flags, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.name = name
        self.sprites = sprites
        self.flags = flags
        self.callbacks = grf.make_callback_manager(grf.HOUSE, callbacks)
        self._props = props

    def get_sprites(self, g):
        res = []

        if self.sprites:
            layouts = []
            for i, sprite in enumerate(self.sprites):
                layouts.append(
                    grf.BasicSpriteLayout(
                        ground={"sprite": grf.SpriteRef(3924, is_global=True)},
                        building={
                            "sprite": grf.SpriteRef(i, is_global=False),
                            "offset": (0, 0),
                            "extent": (16, 16, 16),
                        },
                        feature=grf.HOUSE,
                    )
                )
            assert len(layouts) == 4
            self.callbacks.graphics = grf.RandomSwitch(
                feature=grf.HOUSE, scope="self", triggers=0, lowest_bit=0, cmp_all=False, groups=layouts
            )

        res.append(definition := grf.Define(feature=grf.HOUSE, id=self.id, props={**self._props, "flags": self.flags}))
        if self.sprites:
            res.append(grf.Action1(feature=grf.HOUSE, set_count=len(self.sprites), sprite_count=1))

            for s in self.sprites:
                res.append(s)

        res.extend(self.callbacks.make_map_action(definition))

        return res
