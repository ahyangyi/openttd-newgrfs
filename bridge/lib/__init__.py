import grf
from agrf.lib.bridge import Bridge, BridgeLayout


class ABridge(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, layout: BridgeLayout, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.layout = layout
        self._props = props
        self._agrf_bridge = None

    def name(self, s):
        return s[f"STR_BRIDGE_{self.translation_name}"]

    def get_sprites(self, g):
        if self._agrf_bridge is None:
            s = g.strings
            self._props["purchase_text"] = s[f"STR_BRIDGE_{self.translation_name}_PURCHASE"]
            self._props["description_rail"] = s[f"STR_BRIDGE_{self.translation_name}_DESC_RAIL"]
            self._props["description_road"] = s[f"STR_BRIDGE_{self.translation_name}_DESC_ROAD"]
            self._agrf_bridge = Bridge(id=self.id, name=self.name(s), layout=self.layout, **self._props)

        return self._agrf_bridge.get_sprites(g)
