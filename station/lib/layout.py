import grf
from PIL import Image
import numpy as np
from agrf.graphics import LayeredImage, SCALE_TO_ZOOM
from agrf.magic import CachedFunctorMixin
from agrf.utils import unique_tuple
from grf.sprites import EmptySprite


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

    R = T = L

    @property
    def M(self):
        return ADefaultGroundSprite(self.sprite - 1 if self.sprite % 2 == 0 else self.sprite + 1)

    default_rail = [Image.open("third_party/opengfx2/1012.png"), Image.open("third_party/opengfx2/1011.png")]

    @property
    def sprites(self):
        return []

    def get_fingerprint(self):
        return {"default_ground_sprite": self.sprite}

    def get_resource_files(self):
        return ()


class AGroundSprite(CachedFunctorMixin):
    def __init__(self, sprite, alternatives=None):
        super().__init__()
        self.sprite = sprite
        self.alternatives = alternatives or []

    def to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=0x42D + sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            flags=0,
        )

    def graphics(self, scale, bpp):
        if self.sprite is grf.EMPTY_SPRITE:
            return LayeredImage.empty()
        return LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp))

    def __repr__(self):
        return f"<AGroundSprite:{self.sprite}>"

    def fmap(self, f):
        return AGroundSprite(
            self.sprite if self.sprite is grf.EMPTY_SPRITE else f(self.sprite), [f(s) for s in self.alternatives]
        )

    @property
    def sprites(self):
        return [self.sprite] + self.alternatives

    def get_fingerprint(self):
        return {"ground_sprite": self.sprite.get_fingerprint()}

    def get_resource_files(self):
        return self.sprite.get_resource_files()


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

    @property
    def sprites(self):
        return [self.sprite]

    def get_fingerprint(self):
        return {"parent_sprite": self.sprite.get_fingerprint(), "extent": self.extent, "offset": self.offset}

    def get_resource_files(self):
        return self.sprite.get_resource_files()


class AChildSprite(CachedFunctorMixin):
    def __init__(self, sprite, offset):
        super().__init__()
        self.sprite = sprite
        self.offset = offset

    def __repr__(self):
        return f"<AChildSprite:{self.sprite}:{self.offset}>"

    def to_grf(self, sprite_list):
        return grf.ChildSprite(
            sprite=grf.SpriteRef(
                id=0x42D + sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=True,
                always_transparent=False,
                no_transparent=False,
            ),
            xofs=self.offset[0],
            yofs=self.offset[1],
        )

    def graphics(self, scale, bpp):
        if self.sprite is grf.EMPTY_SPRITE:
            return LayeredImage.empty()
        return LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp))

    def fmap(self, f):
        return AChildSprite(f(self.sprite), self.offset)

    @property
    def sprites(self):
        return [self.sprite]

    def get_fingerprint(self):
        return {"child_sprite": self.sprite.get_fingerprint(), "offset": self.offset}

    def get_resource_files(self):
        return self.sprite.get_resource_files()


def overlaps(a0, a1, b0, b1):
    assert a0 <= a1 and b0 <= b1
    return a1 > b0 and b1 > a0


def is_in_front(a, b):
    ax0, ay0, az0 = a.offset
    ax1, ay1, az1 = (x + y for x, y in zip(a.offset, a.extent))
    bx0, by0, bz0 = b.offset
    bx1, by1, bz1 = (x + y for x, y in zip(b.offset, b.extent))
    if not overlaps(ax0 - az1, ax1 - az0, bx0 - bz1, bx1 - bz0):
        return False
    if not overlaps(ay0 - az1, ay1 - az0, by0 - bz1, by1 - bz0):
        return False
    if not overlaps(ax0 - ay1, ax1 - ay0, bx0 - by1, bx1 - by0):
        return False
    if ax0 >= bx1:
        return True
    if ay0 >= by1:
        return True
    if az0 >= bz1:
        return True
    return False


empty_sprite_1 = EmptySprite()
empty_sprite_2 = EmptySprite()


class ALayout:
    def __init__(self, ground_sprites, parent_sprites, traversable, category=None, notes=None):
        assert isinstance(ground_sprites, list)
        if ground_sprites == []:
            ground_sprites = [AGroundSprite(grf.EMPTY_SPRITE, alternatives=[empty_sprite_1, empty_sprite_2])]
        self.ground_sprites = ground_sprites
        self.parent_sprites = parent_sprites
        self.traversable = traversable
        self.category = category
        self.notes = notes or []

    @property
    def sorted_parent_sprites(self):
        for i in self.parent_sprites:
            for j in self.parent_sprites:
                if i != j:
                    assert not all(
                        i.offset[k] + i.extent[k] > j.offset[k] and j.offset[k] + j.extent[k] > i.offset[k]
                        for k in range(3)
                    ), f"{i} and {j} overlap, {self.parent_sprites}"

        # FIXME include child sprites
        ret = []
        for i in range(len(self.parent_sprites)):
            for j in self.parent_sprites:
                if j in ret:
                    continue
                good = True
                for k in self.parent_sprites:
                    if k != j and k not in ret and is_in_front(j, k):
                        good = False
                        break
                if good:
                    ret.append(j)
                    break
            assert len(ret) == i + 1, f"{self.parent_sprites}, {i}, {ret}"
        return ret

    def to_grf(self, sprite_list):
        return grf.SpriteLayout(
            [sprite.to_grf(sprite_list) for sprite in self.ground_sprites]
            + [sprite.to_grf(sprite_list) for sprite in self.sorted_parent_sprites]
        )

    def graphics(self, scale, bpp, remap=None, context=None):
        context = context or grf.DummyWriteContext()
        img = LayeredImage.empty()
        for sprite in self.ground_sprites:
            new_img = sprite.graphics(scale, bpp).copy()
            img.blend_over(new_img)

        for sprite in self.sorted_parent_sprites:
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
        return f"<ALayout:{self.ground_sprites}:{self.parent_sprites}>"

    def __getattr__(self, name):
        call = lambda x: getattr(x, name)
        new_ground_sprites = [call(sprite) for sprite in self.ground_sprites]
        new_sprites = [call(sprite) for sprite in self.parent_sprites]
        return ALayout(new_ground_sprites, new_sprites, self.traversable, self.category, self.notes)

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ground_sprites = [call(sprite) for sprite in self.ground_sprites]
        new_sprites = [call(sprite) for sprite in self.parent_sprites]
        return ALayout(new_ground_sprites, new_sprites, self.traversable, self.category, self.notes)

    @property
    def sprites(self):
        return list(dict.fromkeys([sub for s in self.ground_sprites + self.parent_sprites for sub in s.sprites]))

    def get_fingerprint(self):
        return {
            "ground_sprites": [s.get_fingerprint() for s in self.ground_sprites],
            "parent_sprites": [s.get_fingerprint() for s in self.parent_sprites],
        }

    def get_resource_files(self):
        return unique_tuple(f for x in self.ground_sprites + self.parent_sprites for f in x.get_resource_files())


class LayoutSprite(grf.Sprite):
    def __init__(self, layout, w, h, scale, bpp, **kwargs):
        super().__init__(w, h, zoom=SCALE_TO_ZOOM[scale], **kwargs)
        self.layout = layout
        self.scale = scale
        self.bpp = bpp

    def get_fingerprint(self):
        return {
            "layout": self.layout.get_fingerprint(),
            "w": self.w,
            "h": self.h,
            "bpp": self.bpp,
            "xofs": self.xofs,
            "yofs": self.yofs,
        }

    def get_resource_files(self):
        return self.layout.get_resource_files()

    def get_data_layers(self, context):
        timer = context.start_timer()
        ret = self.layout.graphics(self.scale, self.bpp)
        ret.resize(self.w, self.h)
        timer.count_composing()

        self.xofs += ret.xofs
        self.yofs += ret.yofs

        return ret.w, ret.h, ret.rgb, ret.alpha, ret.mask
