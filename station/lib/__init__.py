import grf
import numpy as np
from PIL import Image
from agrf.graphics.palette import PIL_PALETTE
from agrf.magic.switch import deep_freeze
from agrf.graphics import LayeredImage, SCALE_TO_ZOOM
from .binary_variants import (
    BuildingSpriteSheetFull,
    BuildingSpriteSheetSymmetrical,
    BuildingSpriteSheetSymmetricalX,
    BuildingSpriteSheetSymmetricalY,
)


class AStation(grf.SpriteGenerator):
    def __init__(self, *, id, translation_name, sprites, layouts, callbacks=None, **props):
        super().__init__()
        self.id = id
        self.translation_name = translation_name
        self.sprites = sprites
        self.layouts = layouts
        if callbacks is None:
            callbacks = {}
        self.callbacks = grf.make_callback_manager(grf.STATION, callbacks)
        self._props = props

    def get_sprites(self, g):
        res = []

        name = g.strings[f"STR_STATION_{self.translation_name}_NAME"]
        class_name = g.strings[f"STR_STATION_CLASS_{self._props['class_label'].decode()}"]

        if self.sprites:
            self.callbacks.graphics = grf.GenericSpriteLayout(ent1=[0], ent2=[0], feature=grf.STATION)

        self.callbacks.set_flag_props(self._props)

        res.append(
            definition := grf.Define(
                feature=grf.STATION,
                id=self.id,
                props={
                    "class_label": self._props["class_label"],
                    "advanced_layout": grf.SpriteLayoutList(self.layouts),
                    **self._props,
                },
            )
        )
        if self.sprites:
            res.append(grf.Action1(feature=grf.STATION, set_count=1, sprite_count=len(self.sprites)))

            for s in self.sprites:
                res.append(s)

        res.extend(self.callbacks.make_map_action(definition))
        res.extend(class_name.get_actions(grf.STATION, 0xC400 + self.id, is_generic_offset=True))
        res.extend(name.get_actions(grf.STATION, 0xC500 + self.id, is_generic_offset=True))

        return res


groundsprite = Image.open("third_party/opengfx2/1012.png")


class Demo:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles

    def graphics(self, remap, scale, bpp):
        yofs = 32 * scale
        img = LayeredImage.canvas(
            -16 * scale * (len(self.tiles) + len(self.tiles[0])),
            -yofs,
            32 * scale * (len(self.tiles) + len(self.tiles[0])),
            yofs + 16 * scale * (len(self.tiles) + len(self.tiles[0])),
            has_mask=remap is None,
        )

        for r, row in enumerate(self.tiles):
            for c, sprite in enumerate(row[::-1]):
                if sprite is None:
                    continue
                subimg = sprite.graphics(remap, scale, bpp)
                img.blend_over(subimg.move((32 * r - 32 * c) * scale, (16 * r + 16 * c) * scale))
        return img

    @property
    def M(self):
        return Demo(self.title, [[tile.M for tile in row[::-1]] for row in list(zip(*self.tiles))[::-1]])


class AMetaStation:
    def __init__(self, stations, class_label, doc_sprites, doc_layouts):
        self.stations = stations
        self.class_label = class_label
        self.doc_sprites = doc_sprites
        self.doc_layouts = doc_layouts

    def add(self, g):
        for station in self.stations:
            g.add(station)


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

    def __repr__(self):
        return f"<ADefaultGroundSprite:{self.sprite}>"

    @property
    def L(self):
        return self

    R = T = TL = TR = L

    @property
    def M(self):
        return ADefaultGroundSprite(self.sprite - 1 if self.sprite % 2 == 0 else self.sprite + 1)


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

    # FIXME add methods


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
    def __init__(self, ground_sprite, sprites):
        self.ground_sprite = ground_sprite
        self.sprites = sprites

    def to_grf(self, sprite_list):
        return grf.SpriteLayout(
            [self.ground_sprite.to_grf(sprite_list)] + [sprite.to_grf(sprite_list) for sprite in self.sprites]
        )

    def graphics(self, remap, scale, bpp, context=grf.DummyWriteContext()):
        img = LayeredImage.empty()
        for sprite in self.sprites:
            masked_sprite = LayeredImage.from_sprite(
                sprite.sprite.get_sprite(zoom=SCALE_TO_ZOOM[scale], bpp=bpp)
            ).copy()
            if remap is not None:
                masked_sprite.remap(remap)
                masked_sprite.apply_mask()

            img.blend_over(
                masked_sprite.move(
                    sprite.offset[0] * scale * 2 + sprite.offset[1] * scale * 2,
                    sprite.offset[0] * scale + sprite.offset[1] * scale,
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
        return ALayout(new_ground_sprite, new_sprites)

    def __call__(self, *args, **kwargs):
        call = lambda x: x(*args, **kwargs)
        new_ground_sprite = call(self.ground_sprite)
        new_sprites = call(self.sprites)
        return ALayout(new_ground_sprite, new_sprites)


class LayoutSprite(grf.Sprite):
    def __init__(self, layout, w, h, scale=4, bpp=32, **kwargs):
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

        import cv2

        cv2.imwrite("rgb.png", ret.rgb)
        cv2.imwrite("alpha.png", ret.alpha)
        cv2.imwrite("mask.png", ret.mask)

        return ret.w, ret.h, ret.rgb, ret.alpha, ret.mask
