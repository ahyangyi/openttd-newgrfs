from dataclasses import dataclass, replace
import grf
from PIL import Image
import functools
import numpy as np
from agrf.graphics import LayeredImage, SCALE_TO_ZOOM
from agrf.magic import CachedFunctorMixin
from agrf.utils import unique_tuple


class ChildSpriteContainerMixin:
    def __init__(self, *args, child_sprites=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.child_sprites = child_sprites or []
        assert all(isinstance(c, AChildSprite) for c in self.child_sprites)

    def to_grf(self, sprite_list):
        return [self.parent_to_grf(sprite_list)] + [cs.to_grf(sprite_list) for cs in self.child_sprites]

    @property
    def sprites_from_child(self):
        return unique_tuple([s for c in self.child_sprites for s in c.sprites])

    def blend_graphics(self, base, scale, bpp, climate="temperate", subclimate="default"):
        for c in self.child_sprites:
            masked_sprite = c.graphics(scale, bpp, climate=climate, subclimate=subclimate)
            base.blend_over(masked_sprite, childsprite=isinstance(self, AParentSprite))


class RegistersMixin:
    def __init__(self, *args, flags=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags = flags or {}

    @property
    def flags_translated(self):
        return {k: (v if k == "add" else v.get_index()) for k, v in self.flags.items() if v is not None}

    def registers_to_grf_dict(self):
        return {"flags": sum(grf.SPRITE_FLAGS[k][1] for k in self.flags.keys()), "registers": self.flags_translated}


class GroundSpriteMixin:
    pass


class BoundingBoxMixin:
    def __init__(self, extent, offset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extent = extent
        self.offset = offset


class DefaultSpriteMixin:
    def __init__(self, sprite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(sprite, int)
        self.sprite = sprite

    climate_dependent_tiles = {
        (climate, k): Image.open(f"third_party/opengfx2/{climate}/{k}.png")
        for climate in ["temperate", "arctic", "tropical", "toyland"]
        for k in [1011, 1012, 1037, 1038, 3981, 4550]
    }
    climate_independent_tiles = {k: Image.open(f"third_party/opengfx2/{k}.png") for k in [1313, 1314, 1420]}

    def graphics(self, scale, bpp, climate="temperate", subclimate="default"):
        # FIXME handle flags correctly
        if self.sprite in self.climate_independent_tiles:
            img = np.asarray(self.climate_independent_tiles[self.sprite])
        else:
            img = np.asarray(
                self.climate_dependent_tiles[(climate, self.sprite + (26 if subclimate != "default" else 0))]
            )
        ret = LayeredImage(-124, 0, 256, 127, img[:, :, :3], img[:, :, 3], None)
        if scale == 4:
            ret = ret.copy()
        elif scale == 2:
            ret.resize(128, 63)
        elif scale == 1:
            ret.resize(64, 31)
        self.blend_graphics(ret, scale, bpp, climate=climate, subclimate=subclimate)
        return ret


class ADefaultGroundSprite(DefaultSpriteMixin, ChildSpriteContainerMixin, RegistersMixin, CachedFunctorMixin):
    def __init__(self, sprite, child_sprites=None, flags=None):
        super().__init__(sprite, child_sprites=child_sprites, flags=flags)

    def parent_to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=self.sprite,
                pal=0,
                is_global=True,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            **self.registers_to_grf_dict(),
        )

    def to_parentsprite(self, low=False):
        if low:
            return ADefaultParentSprite(self.sprite, (16, 16, 0), (0, 0, 0))
        return ADefaultParentSprite(self.sprite, (16, 16, 1), (0, 0, 0))

    def to_action2(self, sprite_list):
        return [{"sprite": grf.SpriteRef(self.sprite, is_global=True)}] + [
            s for x in self.child_sprites for s in x.to_action2(sprite_list)
        ]

    def __repr__(self):
        return f"<ADefaultGroundSprite:{self.sprite}>"

    def fmap(self, f):
        return ADefaultGroundSprite(self.sprite, child_sprites=[f(c) for c in self.child_sprites], flags=self.flags)

    @property
    def M(self):
        return ADefaultGroundSprite(
            self.sprite - 1 if self.sprite % 2 == 0 else self.sprite + 1,
            child_sprites=[c.M for c in self.child_sprites],
            flags=self.flags,
        )

    @property
    def sprites(self):
        return self.sprites_from_child

    def get_fingerprint(self):
        return {"default_ground_sprite": self.sprite}

    def get_resource_files(self):
        return ()

    def __add__(self, child_sprite):
        if child_sprite is None:
            return self
        return ADefaultGroundSprite(
            self.sprite, child_sprites=self.child_sprites + [child_sprite], flags=self.flags.copy()
        )


class AGroundSprite(ChildSpriteContainerMixin, RegistersMixin, CachedFunctorMixin):
    def __init__(self, sprite, alternatives=None, child_sprites=None, flags=None):
        super().__init__(child_sprites=child_sprites, flags=flags)
        self.sprite = sprite
        self.alternatives = alternatives or tuple()

    def parent_to_grf(self, sprite_list):
        return grf.GroundSprite(
            sprite=grf.SpriteRef(
                id=0x42D + sprite_list.index(self.sprite),
                pal=0,
                is_global=False,
                use_recolour=False,
                always_transparent=False,
                no_transparent=False,
            ),
            **self.registers_to_grf_dict(),
        )

    def to_parentsprite(self, low=False):
        if low:
            return AParentSprite(self.sprite, (16, 16, 0), (0, 0, 0))
        return AParentSprite(self.sprite, (16, 16, 1), (0, 0, 0), flags=self.flags)

    def to_action2(self, sprite_list):
        return [{"sprite": grf.SpriteRef(sprite_list.index(self.sprite), is_global=False)}] + [
            s for x in self.child_sprites for s in x.to_action2(sprite_list)
        ]

    def graphics(self, scale, bpp, climate="temperate", subclimate="default"):
        if self.sprite is grf.EMPTY_SPRITE:
            ret = LayeredImage.empty()
        else:
            ret = LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)).copy()
        self.blend_graphics(ret, scale, bpp, climate=climate, subclimate=subclimate)
        return ret

    def __repr__(self):
        return f"<AGroundSprite:{self.sprite}>"

    def fmap(self, f):
        return AGroundSprite(
            self.sprite if self.sprite is grf.EMPTY_SPRITE else f(self.sprite),
            alternatives=tuple(f(s) for s in self.alternatives),
            child_sprites=[f(c) for c in self.child_sprites],
            flags=self.flags,
        )

    @property
    def sprites(self):
        return unique_tuple((self.sprite,) + self.alternatives + self.sprites_from_child)

    def get_fingerprint(self):
        return {"ground_sprite": self.sprite.get_fingerprint()}

    def get_resource_files(self):
        return self.sprite.get_resource_files()

    def __add__(self, child_sprite):
        if child_sprite is None:
            return self
        return AGroundSprite(self.sprite, child_sprites=self.child_sprites + [child_sprite], flags=self.flags.copy())


class ADefaultParentSprite(DefaultSpriteMixin, BoundingBoxMixin, ChildSpriteContainerMixin, RegistersMixin):
    def __init__(self, sprite, extent, offset, child_sprites=None, flags=None):
        super().__init__(sprite, extent, offset, child_sprites=child_sprites, flags=flags)

    def __repr__(self):
        return f"<ADefaultParentSprite:{self.sprite}:{self.extent}:{self.offset}>"

    def parent_to_grf(self, sprite_list):
        return grf.ParentSprite(
            sprite=grf.SpriteRef(
                id=self.sprite, pal=0, is_global=True, use_recolour=True, always_transparent=False, no_transparent=False
            ),
            extent=self.extent,
            offset=self.offset,
            **self.registers_to_grf_dict(),
        )

    def to_action2(self, sprite_list):
        return [
            {"sprite": grf.SpriteRef(self.sprite, is_global=True), "offset": self.offset, "extent": self.extent}
        ] + [s for x in self.child_sprites for s in x.to_action2(sprite_list)]

    def pushdown(self, steps):
        x, y, z = self.offset
        for i in range(steps):
            if z >= 2:
                z -= 2
            else:
                x += 1
                y += 1
        return ADefaultParentSprite(self.sprite, (1, 1, 1), (x, y, z), self.child_sprites, self.flags)

    def demo_translate(self, xofs, yofs, zofs):
        return ADefaultParentSprite(
            self.sprite,
            self.extent,
            (self.offset[0] + xofs * 16, self.offset[1] + yofs * 16, self.offset[2] + zofs * 8),
            self.child_sprites,
            self.flags,
        )

    @functools.cache
    def filter_register(self, reg):
        return ADefaultParentSprite(
            self.sprite,
            self.extent,
            self.offset,
            [x for x in self.child_sprites if x.flags.get("dodraw") != reg],
            self.flags,
        )

    @property
    def L(self):
        return self

    @property
    def M(self):
        mirror = lambda x: (x[1], x[0], x[2])
        return ADefaultParentSprite(
            self.sprite.M,
            mirror(self.extent),
            mirror(self.offset),
            child_sprites=[c.M for c in self.child_sprites],
            flags=self.flags,
        )

    @property
    def R(self):
        new_offset = (16 - self.offset[0] - self.extent[0], self.offset[1], self.offset[2])
        return ADefaultParentSprite(
            self.sprite.R, self.extent, new_offset, child_sprites=[c.R for c in self.child_sprites], flags=self.flags
        )

    @property
    def T(self):
        new_offset = (self.offset[0], 16 - self.offset[1] - self.extent[1], self.offset[2])
        return ADefaultParentSprite(
            self.sprite.T, self.extent, new_offset, child_sprites=[c.T for c in self.child_sprites], flags=self.flags
        )

    @property
    def sprites(self):
        return self.sprites_from_child

    def get_fingerprint(self):
        return {"parent_sprite": self.sprite, "extent": self.extent, "offset": self.offset}

    def get_resource_files(self):
        return []

    def __add__(self, child_sprite):
        if child_sprite is None:
            return self
        return ADefaultParentSprite(
            self.sprite, self.extent, self.offset, child_sprites=self.child_sprites + [child_sprite], flags=self.flags
        )


class AParentSprite(BoundingBoxMixin, ChildSpriteContainerMixin, RegistersMixin):
    def __init__(self, sprite, extent, offset, child_sprites=None, flags=None):
        super().__init__(extent, offset, child_sprites=child_sprites, flags=flags)
        assert isinstance(sprite, grf.ResourceAction)
        self.sprite = sprite

    def __repr__(self):
        return f"<AParentSprite:{self.sprite}:{self.extent}:{self.offset}>"

    def parent_to_grf(self, sprite_list):
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
            **self.registers_to_grf_dict(),
        )

    def to_action2(self, sprite_list):
        return [
            {
                "sprite": grf.SpriteRef(sprite_list.index(self.sprite), is_global=False),
                "offset": self.offset,
                "extent": self.extent,
                **self.flags_translated,
            }
        ] + [s for x in self.child_sprites for s in x.to_action2(sprite_list)]

    def graphics(self, scale, bpp, climate="temperate", subclimate="default"):
        ret = LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)).copy()
        self.blend_graphics(ret, scale, bpp, climate=climate, subclimate=subclimate)
        return ret

    def pushdown(self, steps):
        x, y, z = self.offset
        for i in range(steps):
            if z >= 2:
                z -= 2
            else:
                x += 1
                y += 1
        return AParentSprite(self.sprite, (1, 1, 1), (x, y, z), self.child_sprites, self.flags)

    def demo_translate(self, xofs, yofs, zofs):
        return AParentSprite(
            self.sprite,
            self.extent,
            (self.offset[0] + xofs * 16, self.offset[1] + yofs * 16, self.offset[2] + zofs * 8),
            self.child_sprites,
            self.flags,
        )

    @functools.cache
    def squash(self, ratio):
        return AParentSprite(
            self.sprite.squash(ratio),
            self.extent,
            self.offset,
            [x.squash(ratio) for x in self.child_sprites],
            self.flags,
        )

    @functools.cache
    def filter_register(self, reg):
        return AParentSprite(
            self.sprite,
            self.extent,
            self.offset,
            [x for x in self.child_sprites if x.flags.get("dodraw") != reg],
            self.flags,
        )

    @property
    def L(self):
        return self

    @property
    def M(self):
        mirror = lambda x: (x[1], x[0], x[2])
        return AParentSprite(
            self.sprite.M,
            mirror(self.extent),
            mirror(self.offset),
            child_sprites=[c.M for c in self.child_sprites],
            flags=self.flags,
        )

    @property
    def R(self):
        new_offset = (16 - self.offset[0] - self.extent[0], self.offset[1], self.offset[2])
        return AParentSprite(
            self.sprite.R, self.extent, new_offset, child_sprites=[c.R for c in self.child_sprites], flags=self.flags
        )

    @property
    def T(self):
        new_offset = (self.offset[0], 16 - self.offset[1] - self.extent[1], self.offset[2])
        return AParentSprite(
            self.sprite.T, self.extent, new_offset, child_sprites=[c.T for c in self.child_sprites], flags=self.flags
        )

    @property
    def sprites(self):
        return unique_tuple((self.sprite,) + self.sprites_from_child)

    def get_fingerprint(self):
        return {"parent_sprite": self.sprite.get_fingerprint(), "extent": self.extent, "offset": self.offset}

    def get_resource_files(self):
        return self.sprite.get_resource_files()

    def __add__(self, child_sprite):
        if child_sprite is None:
            return self
        return AParentSprite(
            self.sprite, self.extent, self.offset, child_sprites=self.child_sprites + [child_sprite], flags=self.flags
        )


class AChildSprite(RegistersMixin, CachedFunctorMixin):
    def __init__(self, sprite, offset, flags=None):
        super().__init__(flags=flags)
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
            **self.registers_to_grf_dict(),
        )

    def to_action2(self, sprite_list):
        return [
            {
                "sprite": grf.SpriteRef(sprite_list.index(self.sprite), is_global=False),
                "pixel_offset": self.offset,
                **self.flags_translated,
            }
        ]

    def graphics(self, scale, bpp, climate="temperate", subclimate="default"):
        if self.sprite is grf.EMPTY_SPRITE:
            return LayeredImage.empty()
        # XXX better register handling...?
        from station.lib.registers import Registers

        if self.flags.get("dodraw") == Registers.SNOW and subclimate != "snow":
            return LayeredImage.empty()
        return LayeredImage.from_sprite(self.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp))

    @functools.cache
    def squash(self, ratio):
        return AChildSprite(self.sprite.squash(ratio), self.offset, self.flags)

    def fmap(self, f):
        return AChildSprite(f(self.sprite), self.offset, flags=self.flags)

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


@dataclass(eq=False)
class ALayout:
    ground_sprite: object
    parent_sprites: list
    traversable: bool
    category: str = None
    notes: list = None
    flattened: bool = False
    altitude: int = 0

    def __post_init__(self):
        if self.ground_sprite is None:
            from station.stations.misc import empty_ground

            self.ground_sprite = empty_ground
        assert isinstance(self.ground_sprite, (ADefaultGroundSprite, AGroundSprite))
        assert all(isinstance(s, (ADefaultParentSprite, AParentSprite)) for s in self.parent_sprites), [
            type(s) for s in self.parent_sprites
        ]
        self.notes = self.notes or []

    @property
    def sorted_parent_sprites(self):
        if self.flattened:
            return self.parent_sprites
        for i in self.parent_sprites:
            for j in self.parent_sprites:
                if i != j:
                    assert not all(
                        i.offset[k] + i.extent[k] > j.offset[k] and j.offset[k] + j.extent[k] > i.offset[k]
                        for k in range(3)
                    ), f"{i} and {j} overlap, {self.parent_sprites}"

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

    def pushdown(self, steps):
        from station.stations.misc import empty_ground

        return ALayout(
            empty_ground,
            [s.pushdown(steps) for s in [self.ground_sprite.to_parentsprite()] + self.sorted_parent_sprites],
            self.traversable,
            category=self.category,
            notes=self.notes,
            flattened=True,
            altitude=self.altitude,
        )

    @functools.cache
    def squash(self, ratio):
        return replace(self, parent_sprites=[s.squash(ratio) for s in self.sorted_parent_sprites])

    @functools.cache
    def raise_tile(self, delta=1):
        return replace(self, altitude=self.altitude + delta)

    @functools.cache
    def lower_tile(self, delta=1):
        return self.raise_tile(-delta)

    @functools.cache
    def filter_register(self, reg):
        return replace(
            self, parent_sprites=[s.filter_register(reg) for s in self.parent_sprites if s.flags.get("dodraw") != reg]
        )

    @functools.cache
    def demo_translate(self, xofs, yofs):
        from station.stations.misc import empty_ground

        return replace(
            self,
            ground_sprite=empty_ground,
            parent_sprites=[
                s.demo_translate(xofs, yofs, self.altitude)
                for s in [self.ground_sprite.to_parentsprite(low=True)] + self.sorted_parent_sprites
            ],
            altitude=0,
        )

    def to_grf(self, sprite_list):
        if self.flattened:
            parent_sprites = self.parent_sprites
        else:
            parent_sprites = self.sorted_parent_sprites
        return grf.SpriteLayout(
            [s for s in self.ground_sprite.to_grf(sprite_list)]
            + [s for sprite in parent_sprites for s in sprite.to_grf(sprite_list)]
        )

    def to_action2(self, feature, sprite_list):
        ground = self.ground_sprite.to_action2(sprite_list)
        buildings = [s for sprite in self.sorted_parent_sprites for s in sprite.to_action2(sprite_list)]
        return grf.AdvancedSpriteLayout(ground=ground[0], feature=feature, buildings=tuple(ground[1:] + buildings))

    def graphics(self, scale, bpp, remap=None, context=None, climate="temperate", subclimate="default"):
        context = context or grf.DummyWriteContext()
        img = LayeredImage.empty()

        new_img = self.ground_sprite.graphics(scale, bpp, climate=climate, subclimate=subclimate).copy()
        img.blend_over(new_img)

        for sprite in self.sorted_parent_sprites:
            masked_sprite = sprite.graphics(scale, bpp, climate=climate, subclimate=subclimate)
            if remap is not None:
                masked_sprite.remap(remap)
                masked_sprite.apply_mask()

            img.blend_over(
                masked_sprite.move(
                    (-sprite.offset[0] * 2 + sprite.offset[1] * 2) * scale,
                    (sprite.offset[0] + sprite.offset[1] - sprite.offset[2]) * scale,
                )
            )

        return img.move(0, -self.altitude * 8 * scale)

    def to_index(self, layout_pool):
        return layout_pool.index(self)

    def __repr__(self):
        return f"<ALayout:{self.ground_sprite}:{self.parent_sprites}>"

    def __getattr__(self, name):
        call = lambda x: getattr(x, name)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = [call(sprite) for sprite in self.parent_sprites]
        return ALayout(
            new_ground_sprite, new_sprites, self.traversable, self.category, self.notes, altitude=self.altitude
        )

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = [call(sprite) for sprite in self.parent_sprites]
        return ALayout(
            new_ground_sprite, new_sprites, self.traversable, self.category, self.notes, altitude=self.altitude
        )

    @property
    def sprites(self):
        return list(dict.fromkeys([sub for s in [self.ground_sprite] + self.parent_sprites for sub in s.sprites]))

    def get_fingerprint(self):
        return {
            "ground_sprite": self.ground_sprite.get_fingerprint(),
            "parent_sprites": [s.get_fingerprint() for s in self.parent_sprites],
        }

    def get_resource_files(self):
        return unique_tuple(f for x in [self.ground_sprite] + self.parent_sprites for f in x.get_resource_files())


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
