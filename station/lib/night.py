import grf
from dataclasses import replace
from station.lib.parameters import nightgfx
from agrf.lib.building.layout import (
    ALayout,
    NewGeneralSprite,
    AChildSprite,
    NightSprite,
    OffsetPosition,
    DefaultGraphics,
    NewGraphics,
)
from agrf.graphics.misc import SCALE_TO_ZOOM


class SquashableAlternativeSprites(grf.AlternativeSprites):
    def __init__(self, old_alt, darkness=0.75):
        super().__init__(
            *[
                NightSprite(old_alt, 64 * scale, 64 * scale, xofs=0, yofs=0, scale=scale, bpp=bpp, darkness=darkness)
                for scale in [1, 2, 4]
                for bpp in [8, 32]
                if (s := old_alt.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)) is not None
            ]
        )
        self.darkness = darkness
        self.old_alt = old_alt

    def squash(self, ratio):
        x = self.old_alt.squash(ratio)
        return SquashableAlternativeSprites(self.old_alt.squash(ratio), self.darkness)

    def get_fingerprint(self):
        return {"old_alt": self.old_alt.get_fingerrint()}


def make_child_night_masks(parent, darkness=0.75):
    if isinstance(parent, DefaultGraphics):
        return []
    assert isinstance(parent, NewGraphics)
    night = parent.sprite.symmetry_fmap(lambda x: SquashableAlternativeSprites(x, darkness))
    return [AChildSprite(night, (0, 0), flags={"dodraw": nightgfx})]


def add_night_masks(thing, darkness=0.75):
    if isinstance(thing, ALayout):
        ret = replace(
            thing,
            ground_sprite=add_night_masks(thing.ground_sprite, darkness=darkness),
            parent_sprites=[add_night_masks(p, darkness=darkness) for p in thing.parent_sprites],
        )
        ret.__class__ = ALayout
        return ret
    if isinstance(thing, NewGeneralSprite):
        assert not isinstance(thing.position, OffsetPosition), thing
        new_child_sprites = make_child_night_masks(thing.sprite)
        for x in thing.child_sprites:
            new_child_sprites.append(x)
            new_child_sprites.extend(make_child_night_masks(x.sprite))

        return replace(thing, child_sprites=new_child_sprites)

    raise NotImplementedError()
