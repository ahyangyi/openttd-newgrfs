import grf
from PIL import Image
import numpy as np
from agrf.graphics import LayeredImage, SCALE_TO_ZOOM


class ADefaultGroundSprite:
    def __init__(self, sprite):
        self.sprite = sprite

    def to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=self.sprite,
                pal=0,
                is_global=True,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        )

    def graphics(self, scale, bpp):
        if self.sprite not in [1012, 1011]:
            return LayeredImage.empty()
        img = np.asarray(ADefaultGroundSprite.default_rail[1012 - self.sprite])
        ret = LayeredImage(-128, 0, 256, 127, img[:, :, :3], img[:, :, 3], None)
        if scale == 2:
            ret.resize(128, 63)
        elif scale == 1:
            ret.resize(64, 31)
        return ret

    def __repr__(self):
        return f"<ADefaultGroundSprite:{self.sprite}>"

    @property
    def L(self):
        return self

    R = T = TL = TR = L

    @property
    def M(self):
        return ADefaultGroundSprite(self.sprite - 1 if self.sprite % 2 == 0 else self.sprite + 1)

    default_rail = [Image.open("third_party/opengfx2/1012.png"), Image.open("third_party/opengfx2/1011.png")]


class AGroundSprite:
    def __init__(self, sprite):
        self.sprite = sprite

    def to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        )

    def graphics(self, scale, bpp):
        return LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp))

    def __getattr__(self, name):
        return AGroundSprite(getattr(self.sprite, name))

    def __call__(self, *args, **kwargs):
        return AGroundSprite(self.sprite(*args, **kwargs))


class AParentSprite:
    def __init__(self, sprite, extent, offset):
        self.sprite = sprite
        self.extent = extent
        self.offset = offset

    def __repr__(self):
        return f"<AParentSprite:{self.sprite}:{self.extent}:{self.offset}>"

    def to_grf(self, sprite_list):
        return grf.ParentSprite(
            sprite=grf.SpriteRef(
                id=0x42D + sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=True,
                always_transparent=False,
                no_transparent=False,
            ),
            extent=self.extent,
            offset=self.offset,
            flags=0,
        )

    @property
    def L(self):
        return self

    @property
    def M(self):
        mirror = lambda x: (x[1], x[0], x[2])
        return AParentSprite(self.sprite.M, mirror(self.extent), mirror(self.offset))

    @property
    def R(self):
        new_offset = (16 - self.offset[0] - self.extent[0], self.offset[1], self.offset[2])
        return AParentSprite(self.sprite.R, self.extent, new_offset)

    @property
    def T(self):
        new_offset = (self.offset[0], 16 - self.offset[1] - self.extent[1], self.offset[2])
        return AParentSprite(self.sprite.T, self.extent, new_offset)

    TL = T

    @property
    def TR(self):
        return self.T.R


class ALayout:
    def __init__(self, ground_sprite, sprites, traversable, category=None, notes=None):
        self.ground_sprite = ground_sprite
        self.sprites = sprites
        self.traversable = traversable
        self.category = category
        self.notes = notes or []

    def to_grf(self, sprite_list):
        return grf.SpriteLayout(
            [self.ground_sprite.to_grf(sprite_list)] + [sprite.to_grf(sprite_list) for sprite in self.sprites]
        )

    def graphics(self, remap, scale, bpp, context=grf.DummyWriteContext()):
        img = self.ground_sprite.graphics(scale, bpp).copy()
        for sprite in self.sprites:
            masked_sprite = LayeredImage.from_sprite(
                sprite.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)
            ).copy()
            if remap is not None:
                masked_sprite.remap(remap)
                masked_sprite.apply_mask()

            img.blend_over(
                masked_sprite.move(
                    (-sprite.offset[0] * 2 + sprite.offset[1] * 2) * scale,
                    (sprite.offset[0] + sprite.offset[1] - sprite.offset[2]) * scale,
                )
            )
        return img

    def to_index(self, layout_pool):
        return layout_pool.index(self)

    def __repr__(self):
        return f"<ALayout:{self.ground_sprite}:{self.sprites}>"

    def __getattr__(self, name):
        call = lambda x: getattr(x, name)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = [call(sprite) for sprite in self.sprites]
        return ALayout(new_ground_sprite, new_sprites, self.traversable)

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = call(self.sprites)
        return ALayout(new_ground_sprite, new_sprites, self.traversable)


class LayoutSprite(grf.Sprite):
    def __init__(self, layout, w, h, scale, bpp, **kwargs):
        super().__init__(w, h, zoom=SCALE_TO_ZOOM[scale], **kwargs)
        self.layout = layout
        self.scale = scale
        self.bpp = bpp

    def get_fingerprint(self):
        # FIXME don't use id
        return {"layout": id(self.layout), "w": self.w, "h": self.h, "bpp": self.bpp}

    def get_image_files(self):
        return ()

    def get_data_layers(self, context):
        timer = context.start_timer()
        ret = self.layout.graphics(None, self.scale, self.bpp)
        ret.resize(self.w, self.h)
        timer.count_composing()

        self.xofs += ret.xofs
        self.yofs += ret.yofs

        return ret.w, ret.h, ret.rgb, ret.alpha, ret.mask
