import grf
from dataclasses import replace
from station.lib.parameters import nightgfx
from agrf.lib.building.layout import ALayout, NewGeneralSprite, AChildSprite, NightSprite
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


def make_child_night_mask(parent, darkness=0.75):
    night = parent.sprite.symmetry_fmap(lambda x: SquashableAlternativeSprites(x, darkness))
    return AChildSprite(night.sprite, (0, 0), flags={"dodraw": nightgfx})


def add_night_masks(thing, darkness=0.75):
    if isinstance(thing, ALayout):
        return replace(
            thing,
            ground_sprite=add_night_masks(thing.ground_sprite, darkness=darkess),
            parent_sprites=[add_night_masks(p, darkness=darkness) for p in self.parent_sprites],
        )
    if isinstance(thing, NewGeneralSprite):
        return replace(thing, child_sprites=make_child_night_mask(thing.sprite) + thing.child_sprite)

    raise NotImplementedError()
