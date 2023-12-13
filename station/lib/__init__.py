import grf


class AStation(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, sprites, callbacks={}, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.sprites = sprites
        self.callbacks = grf.make_callback_manager(grf.STATION, callbacks)
        self._props = props

    def get_sprites(self, g):
        res = []

        name = g.strings[f"STR_STATION_{self.translation_name}_NAME"]

        if self.sprites:
            layouts = []
            for i, sprite in enumerate(self.sprites):
                layouts.append(grf.GenericSpriteLayout(ent1=[i], ent2=[i], feature=grf.STATION))
            assert len(layouts) == 12
            self.callbacks.graphics = layouts[0]

        res.append(
            definition := grf.Define(
                feature=grf.STATION, id=self.id, props={"class_label": self._props["class_label"], **self._props}
            )
        )
        if self.sprites:
            res.append(grf.Action1(feature=grf.STATION, set_count=len(self.sprites), sprite_count=1))

            for s in self.sprites:
                res.append(s)

        res.extend(self.callbacks.make_map_action(definition))

        return res
