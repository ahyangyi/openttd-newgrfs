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
from .layout import ADefaultGroundSprite, AGroundSprite, AParentSprite, ALayout
from .metastation import AMetaStation
from .utils import class_label_printable


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

    @property
    def class_label_plain(self):
        return class_label_printable(self._props["class_label"])

    def get_sprites(self, g):
        res = []

        name = g.strings[f"STR_STATION_{self.translation_name}_NAME"]
        class_name = g.strings[f"STR_STATION_CLASS_{self.class_label_plain}"]

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
