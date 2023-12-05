import grf
from dataclasses import dataclass
from typing import Tuple


@dataclass
class SpritePair:
    X: grf.SpriteRef | grf.ResourceAction
    Y: grf.SpriteRef | grf.ResourceAction


@dataclass
class ASingleTypeBridgeLayout:
    back: Tuple[SpritePair, SpritePair, SpritePair, SpritePair, SpritePair, SpritePair]
    front: Tuple[SpritePair, SpritePair, SpritePair, SpritePair, SpritePair, SpritePair]
    pillars: Tuple[SpritePair, SpritePair, SpritePair, SpritePair, SpritePair, SpritePair]
    flat: Tuple[SpritePair, SpritePair]
    ramp: Tuple[SpritePair, SpritePair]

    @staticmethod
    def one_grid_layout(back, front, pillars, flat, ramp):
        return ASingleTypeBridgeLayout((back,) * 6, (front,) * 6, (pillars,) * 6, flat, ramp)


@dataclass
class ABridgeLayout:
    rail: ASingleTypeBridgeLayout
    road: ASingleTypeBridgeLayout
    mono: ASingleTypeBridgeLayout
    mlev: ASingleTypeBridgeLayout

    @staticmethod
    def make_universal(single_layout):
        return ABridgeLayout(
            rail=single_layout,
            road=single_layout,
            mono=single_layout,
            mlev=single_layout,
        )


class ABridge(grf.SpriteGenerator):
    def __init__(
        self,
        *,
        id,
        name,
        layout: ABridgeLayout,
        purchase_text=None,
        description_rail=None,
        description_road=None,
        **props,
    ):
        super().__init__()
        self.id = id
        self.name = name
        self.layout = layout
        self.purchase_text = purchase_text
        self.description_rail = description_rail
        self.description_road = description_road
        self._props = props

        # FIXME: supprt new layout abstraction
        self._props["layout"] = layout

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
