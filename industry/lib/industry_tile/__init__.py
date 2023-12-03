import grf


class AIndustryTile(grf.SpriteGenerator):
    def __init__(self, *, id, sprites, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.sprites = sprites
        self._props = props
        self.callbacks = grf.make_callback_manager(grf.INDUSTRY_TILE, callbacks)

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
                        feature=grf.INDUSTRY_TILE,
                    )
                )
            assert len(layouts) == 4
            self.callbacks.graphics = grf.RandomSwitch(
                feature=grf.INDUSTRY_TILE, scope="self", triggers=0, lowest_bit=0, cmp_all=False, groups=layouts
            )
        res.append(definition := grf.Define(feature=grf.INDUSTRY_TILE, id=self.id, props=self._props))

        if self.sprites:
            res.append(grf.Action1(feature=grf.INDUSTRY_TILE, set_count=len(self.sprites), sprite_count=1))

            for s in self.sprites:
                res.append(s)

        res.extend(self.callbacks.make_map_action(definition))

        return res
