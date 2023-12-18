from agrf.lib.road_type import RoadType, TramType


class TranslationMixin:
    def __init__(self, id, translation_name, **kwargs):
        self.translation_name = translation_name
        super().__init__(id=id, **kwargs)

    def get_sprites(self, g):
        s = g.strings

        self._props["toolbar_caption"] = self._props["menu_text"] = s[f"STR_RT_{self.translation_name}_CONS"]
        self._props["name"] = s[f"STR_RT_{self.translation_name}_NAME"]
        return super().get_sprites(g)


class ARoadType(TranslationMixin, RoadType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ATramType(TranslationMixin, TramType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
