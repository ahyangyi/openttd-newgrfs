import grf


class ABridge(grf.SpriteGenerator):
    def __init__(
        self,
        *,
        id,
        name,
        back,
        front,
        pillar,
        purchase_text=None,
        description_rail=None,
        description_road=None,
        **props,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.back = back
        self.front = front
        self.pillar = pillar
        self.purchase_text = purchase_text
        self.description_rail = description_rail
        self.description_road = description_road
        self._props = props

    def get_sprites(self, g):
        extra_props = {}
        if self.purchase_text:
            extra_props["purchase_text"] = g.strings.add(self.purchase_text).get_persistent_id()
        if self.description_rail:
            extra_props["description_rail"] = g.strings.add(self.description_rail).get_persistent_id()
        if self.description_road:
            extra_props["description_road"] = g.strings.add(self.description_road).get_persistent_id()

        res = []

        if isinstance(self.name, grf.StringRef):
            name_action = self.name.get_actions(grf.BRIDGE, self.id)
        else:
            name_action = g.strings.add(self.name).get_actions(grf.BRIDGE, self.id)

        res.extend(name_action)
        res.append(definition := grf.Define(feature=grf.BRIDGE, id=self.id, props={**self._props, **extra_props}))

        return res
