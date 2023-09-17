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
        res.append(definition := grf.Define(feature=grf.INDUSTRY_TILE, id=self.id, props=self._props))
        self.callbacks.graphics = 0
        res.append(self.callbacks.make_map_action(definition))

        return res
