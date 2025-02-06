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
from agrf.graphics.misc import SCALE_TO_ZOOM
from agrf.sprites.empty import EmptyAlternativeSprites


class SquashableAlternativeSprites(grf.AlternativeSprites):
    def __init__(self, old_alt, darkness=0.75):
        sprites = []
        for scale in [1, 2, 4]:
            for bpp in [8, 32]:
                if (s := old_alt.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)) is not None:
                    if (
                        "agrf_childsprite" in old_alt.voxel.config
                        or "agrf_relative_childsprite" in old_alt.voxel.config
                    ):
                        xofs, yofs = s.xofs, s.yofs
                    else:
                        xofs, yofs = 0, 0
                    sprites.append(
                        NightSprite(
                            old_alt,
                            64 * scale,
                            64 * scale,
                            xofs=xofs,
                            yofs=yofs,
                            scale=scale,
                            bpp=bpp,
                            darkness=darkness,
                        )
                    )

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


NIGHT_CACHE = {}


def make_child_night_masks(parent, darkness=0.75):
    if parent in NIGHT_CACHE:
        return NIGHT_CACHE[parent]
    graphics = parent.sprite
    if isinstance(graphics, DefaultGraphics):
        return []
    assert isinstance(graphics, NewGraphics)

    if isinstance(graphics.sprite, EmptyAlternativeSprites):
        return []

    if parent.flags.get("dodraw") is None:
        flags = {"dodraw": Registers.NIGHTGFX}
    elif parent.flags.get("dodraw") == Registers.SNOW:
        flags = {"dodraw": Registers.SNOW_NIGHTGFX}
    else:
        raise NotImplementedError(parent.flags["dodraw"])

    night = graphics.sprite.symmetry_fmap(lambda x: SquashableAlternativeSprites(x, darkness))
    return (NIGHT_CACHE[parent] := [AChildSprite(night, (0, 0), flags=flags)])


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
        new_child_sprites = make_child_night_masks(thing)
        for x in thing.child_sprites:
            new_child_sprites.append(x)
            new_child_sprites.extend(make_child_night_masks(x))

        return replace(thing, child_sprites=new_child_sprites)

    raise NotImplementedError()
