import grf
from station.lib.utils import class_label_printable
from agrf.magic import Switch


class AObject(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, layouts, callbacks=None, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.layouts = layouts
        if callbacks is None:
            callbacks = {}
        self.callbacks = grf.make_callback_manager(grf.OBJECT, callbacks)
        self._props = props

    @property
    def class_label_plain(self):
        return class_label_printable(self._props["class_label"])

    def get_sprites(self, g, sprites=None):
        res = []

        extra_props = {"name_id": 0x5801, "class_name_id": 0x5801}
        # extra_props = {
        #    "name_id": g.strings.add(g.strings[f"STR_OBJECT_{self.translation_name}"]).get_persistent_id(),
        #    "class_name_id": g.strings.add(g.strings[f"STR_OBJECT_CLASS_{self.class_label_plain}"]).get_persistent_id(),
        # }

        if sprites is None:
            sprites = self.sprites
            res.append(grf.Action1(feature=grf.OBJECT, set_count=len(self.sprites), sprite_count=1))

            for s in self.sprites:
                res.append(s)

        layouts = []
        for i, layout in enumerate(self.layouts):
            layouts.append(layout.to_action2(feature=grf.OBJECT, sprite_list=sprites))
        self.callbacks.graphics = Switch(
            ranges={i: layouts[i] for i in range(len(layouts))}, default=layouts[0], code="view"
        )
        self.callbacks.set_flag_props(self._props)

        res.append(
            definition := grf.Object(
                id=self.id, **{"class_label": self._props["class_label"], **self._props, **extra_props}
            )
        )

        res.extend(self.callbacks.make_map_action(definition))

        return res

    @property
    def sprites(self):
        return [*dict.fromkeys([sub for l in self.layouts for sub in l.sprites])]