import grf
from .utils import class_label_printable


class AStation(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, layouts, callbacks=None, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.layouts = layouts
        if callbacks is None:
            callbacks = {}
        self.callbacks = grf.make_callback_manager(grf.STATION, callbacks)
        self._props = props

    @property
    def class_label_plain(self):
        return class_label_printable(self._props["class_label"])

    def get_sprites(self, g, sprites=None):
        res = []

        extra_props = {
            "station_name": g.strings.add(g.strings[f"STR_STATION_{self.translation_name}"]).get_persistent_id(),
            "station_class_name": g.strings.add(
                g.strings[f"STR_STATION_CLASS_{self.class_label_plain}"]
            ).get_persistent_id(),
        }

        self.callbacks.graphics = grf.GenericSpriteLayout(ent1=[0], ent2=[0], feature=grf.STATION)
        self.callbacks.set_flag_props(self._props)

        if sprites is None:
            sprites = self.sprites
            res.append(grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(self.sprites)))

            for s in self.sprites:
                res.append(s)

        res.append(
            definition := grf.Define(
                feature=grf.STATION,
                id=self.id,
                props={
                    "class_label": self._props["class_label"],
                    "advanced_layout": grf.SpriteLayoutList([l.to_grf(sprites) for l in self.layouts]),
                    **self._props,
                },
            )
        )
        g.add(grf.If(is_static=True, variable=0xA1, condition=0x04, value=0x1E000000, skip=1, varsize=4))
        res.append(grf.Define(feature=grf.STATION, id=self.id, props=extra_props))

        res.extend(self.callbacks.make_map_action(definition))

        return res

    @property
    def sprites(self):
        return [*dict.fromkeys([sub for l in self.layouts for sub in l.sprites])]
