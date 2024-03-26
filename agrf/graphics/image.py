from .palette import NUMPY_PALETTE
from PIL import Image


# An intermediate representation of image, based on grf.Sprite.get_data_layers()
# Most non-IO methods are in-place for performance purposes
class LayeredImage:
    def __init__(self, xofs, yofs, w, h, rgb, alpha, mask):
        self.xofs = xofs
        self.yofs = yofs
        self.w = w
        self.h = h
        self.rgb = rgb
        self.alpha = alpha
        self.mask = mask

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
        mask_colour = NUMPY_PALETTE[self.mask].astype("uint16")
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
