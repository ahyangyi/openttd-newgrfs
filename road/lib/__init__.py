from agrf.lib.road_type import RoadType


class ARoadType(RoadType):
    def __init__(self, *, id, translation_name, underlay, **props):
        self.translation_name = translation_name
        super().__init__(
            id=id,
            underlay=underlay,
            **props,
        )

    def get_sprites(self, g):
        s = g.strings

        self._props["toolbar_caption"] = self._props["menu_text"] = s[f"STR_RT_{self.translation_name}_CONS"]
        self._props["name"] = s[f"STR_RT_{self.translation_name}_NAME"]
        return super().get_sprites(g)
