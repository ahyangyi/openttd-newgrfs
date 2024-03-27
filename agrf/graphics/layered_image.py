import grf
from .palette import NUMPY_PALETTE
from PIL import Image


# An intermediate representation of image, based on grf.Sprite.get_data_layers()
# Most non-IO methods are in-place for `self` for performance purposes, but will not change `other`
class LayeredImage:
    def __init__(self, xofs, yofs, w, h, rgb, alpha, mask):
        self.xofs = xofs
        self.yofs = yofs
        self.w = w
        self.h = h
        self.rgb = rgb
        self.alpha = alpha
        self.mask = mask

    @staticmethod
    def from_sprite(sprite, context=None):
        context = context or grf.DummyWriteContext()
        w, h, rgb, alpha, mask = sprite.get_data_layers(self, context)
        return LayeredImage(sprite.xofs, sprite.yofs, w, h, rgb, alpha, mask)

    def copy(self):
        return Image(
            self.xofs,
            self.yofs,
            self.w,
            self.h,
            self.rgb and self.rgb.copy(),
            self.alpha and self.alpha.copy(),
            self.mask and self.mask.copy(),
        )

    def apply_mask(self):
        if self.mask is None:
            return
        v = np.min(self.rgb, axis=2, keepdims=True)
        mask_colour = NUMPY_PALETTE[self.mask].astype(np.uint16)
        mask_colour *= v
        mask_colour //= 2**7
        r_ob = np.maximum(mask_colour[:, :, 0], 255) - 255
        g_ob = np.maximum(mask_colour[:, :, 1], 255) - 255
        b_ob = np.maximum(mask_colour[:, :, 2], 255) - 255
        ob = (r_ob + g_ob + b_ob) // 2

        above = mask_colour >= 255
        below = np.minimum(mask_colour + ob[:, :, np.newaxis] * (255 - mask_colour) // 256, 255)
        mixed = np.where(above, 255, below)

        mixed[:, :, 3] = self.rgb
        mask_pal = self.mask == 0
        blended = np.where(np.broadcast_to(mask_pal[:, :, np.newaxis], (*mask_pal.shape, 3)), self.rgb, mixed)

        self.rgb = blended
        self.mask = None

    def adjust_canvas(self, other):
        # x: other.xofs - self.xofs .. other.w - 1 + other.xofs - self.xofs
        # y: other.yofs - self.yofs .. other.h - 1 + other.yofs - self.yofs
        w = max(other.w + other.xofs - self.xofs, self.w) - min(0, other.xofs - self.xofs)
        h = max(other.h + other.yofs - self.yofs, self.h) - min(0, other.yofs - self.yofs)
        x0 = max(0, self.xofs - other.xofs)
        y0 = max(0, self.yofs - other.yofs)
        if w == self.w or h == self.h:
            return

        if self.rgb is not None:
            new_rgb = np.zeros((h, w, 3), dtype=np.uint8)
            new_rgb[y0 : y0 + self.h, x0 : x0 + self.w] = self.rgb
            self.rgb = new_rgb

        if self.alpha is not None:
            new_alpha = np.zeros((h, w), dtype=np.uint8)
            new_alpha[y0 : y0 + self.h, x0 : x0 + self.w] = self.alpha
            self.alpha = new_alpha

        if self.mask is not None:
            new_mask = np.zeros((h, w), dtype=np.uint8)
            new_mask[y0 : y0 + self.h, x0 : x0 + self.w] = self.mask
            self.mask = new_mask

        self.w = w
        self.h = h
        self.xofs -= x0
        self.yofs -= y0

    def blend_over(self, other):
        self.adjust_canvas(other)

        x1 = other.xofs - self.xofs
        y1 = other.yofs - self.yofs

        if self.mask is not None:
            mask_viewport = self.mask[y1 : y1 + other.h, x1 : x1 + other.w]
            if self.rgb is None:
                opacity = other.mask != 0
            else:
                opacity = other.alpha != 0
            view_mask[:, :] = view_mask * (1 - opacity) + other.mask * opacity

        if self.rgb is not None:
            rgb_viewport = self.rgb[y1 : y1 + other.h, x1 : x1 + other.w]
            alpha_viewport = self.alpha[y1 : y1 + other.h, x1 : x1 + other.w]

            alpha1 = alpha_viewport.astype(np.uint32)
            alpha2 = other.alpha.astype(np.uint32)
            alpha1_component = alpha1 * (255 - alpha2)
            alpha2_component = alpha2 * 255
            new_alpha = alpha1_component + alpha2_component
            rgb_viewport[:, :] = (
                alpha1_component * rgb_viewport + alpha2_component * other.rgb + new_alpha // 2
            ) // np.maximum(new_alpha, 1)
            alpha_viewport[:, :] = (new_alpha + 128) // 255
