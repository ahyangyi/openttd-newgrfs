import grf
from dataclasses import replace
from station.lib.registers import Registers
from agrf.lib.building.layout import (
    ALayout,
    NewGeneralSprite,
    AChildSprite,
    NightSprite,
    OffsetPosition,
    DefaultGraphics,
    NewGraphics,
)
from agrf.lib.building.symmetry import BuildingSymmetryMixin
from agrf.graphics.misc import SCALE_TO_ZOOM
from agrf.sprites.empty import EmptyAlternativeSprites


class SquashableAlternativeSprites(grf.AlternativeSprites):
    def __init__(self, old_alt, automatic_offset_mode, darkness):
        sprites = []
        for scale in [1, 2, 4]:
            for bpp in [32]:
                if (s := old_alt.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)) is not None:
                    sprites.append(
                        NightSprite(
                            old_alt,
                            s.w,
                            s.h,
                            scale=scale,
                            base_bpp=bpp,
                            automatic_offset_mode=automatic_offset_mode,
                            darkness=darkness,
                        )
                    )

        super().__init__(*sprites)
        self.old_alt = old_alt
        self.automatic_offset_mode = automatic_offset_mode
        self.darkness = darkness

    def squash(self, ratio):
        x = self.old_alt.squash(ratio)
        return SquashableAlternativeSprites(self.old_alt.squash(ratio), self.automatic_offset_mode, self.darkness)

    def get_fingerprint(self):
        return {"old_alt": self.old_alt.get_fingerrint()}


NIGHT_CACHE = {}


def make_child_night_masks(parent, automatic_offset_mode, darkness):
    if id(parent) in NIGHT_CACHE:
        return NIGHT_CACHE[id(parent)]
    graphics = parent.sprite
    if isinstance(graphics, DefaultGraphics):
        return []
    assert isinstance(graphics, NewGraphics)

    if isinstance(graphics.sprite, EmptyAlternativeSprites):
        return []
    if graphics.sprite is grf.EMPTY_SPRITE:
        return []

    if parent.flags.get("dodraw") is None:
        flags = {"dodraw": Registers.NIGHTGFX}
    elif parent.flags.get("dodraw") == Registers.SNOW:
        flags = {"dodraw": Registers.SNOW_NIGHTGFX}
    else:
        raise NotImplementedError(parent.flags["dodraw"])

    f = lambda x: SquashableAlternativeSprites(x, automatic_offset_mode, darkness=darkness)
    if isinstance(graphics.sprite, BuildingSymmetryMixin):
        night = graphics.sprite.symmetry_fmap(f)
    else:
        night = f(graphics.sprite)

    NIGHT_CACHE[id(parent)] = [AChildSprite(night, (0, 0), flags=flags)]
    return NIGHT_CACHE[id(parent)]


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
        assert not any(isinstance(x.sprite, SquashableAlternativeSprites) for x in thing.child_sprites)
        new_child_sprites = make_child_night_masks(thing, "parent", darkness=darkness).copy()
        for x in thing.child_sprites:
            new_child_sprites.append(x)
            new_child_sprites.extend(make_child_night_masks(x, "child", darkness=darkness))

        return replace(thing, child_sprites=new_child_sprites)

    raise NotImplementedError()
