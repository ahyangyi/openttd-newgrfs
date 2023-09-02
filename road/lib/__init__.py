import grf


class ARoadType(grf.SpriteGenerator):
    def __init__(self, *, id, name, underlay, toolbar_caption=None, **props):
        super().__init__()
        self.id = id
        self.name = name
        self.underlay = underlay
        self.toolbar_caption = toolbar_caption
        self._props = props

    def get_sprites(self, g):
        extra_props = {}
        if self.toolbar_caption:
            extra_props["toolbar_caption"] = g.strings.add(self.toolbar_caption).get_persistent_id()

        res = []

        if self.underlay:
            layouts = []
            for i, sprite in enumerate(self.underlay):
                layouts.append(
                    grf.GenericSpriteLayout(
                        ent1=(i,),
                        ent2=(i,),
                        feature=grf.ROADTYPE,
                    )
                )

        if isinstance(self.name, grf.StringRef):
            name_action = self.name.get_actions(grf.ROADTYPE, self.id)
        else:
            name_action = g.strings.add(self.name).get_actions(grf.ROADTYPE, self.id)

        res.extend(name_action)
        res.append(definition := grf.Define(feature=grf.ROADTYPE, id=self.id, props={**self._props, **extra_props}))
        if self.underlay:
            res.append(
                grf.Action1(
                    feature=grf.ROADTYPE,
                    set_count=1,
                    sprite_count=19,
                )
            )

            for s in self.underlay:
                res.append(s)

        res.append(
            grf.Map(
                definition=definition,
                maps={
                    0x02: layouts[0],
                },
                default=layouts[0],
            )
        )

        return res
