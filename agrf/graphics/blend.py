from PIL import Image, ImageChops
import numpy as np


def blend(image, mask):
    v = ImageChops.lighter(ImageChops.lighter(image.getchannel("R"), image.getchannel("G")), image.getchannel("B"))
    mask_colour = np.uint16(mask.convert("RGBA"))
    mask_colour *= np.uint16(v)[:, :, np.newaxis]
    mask_colour //= 2**7
    r_ob = np.maximum(mask_colour[:, :, 0], 255) - 255
    g_ob = np.maximum(mask_colour[:, :, 1], 255) - 255
    b_ob = np.maximum(mask_colour[:, :, 2], 255) - 255
    ob = (r_ob + g_ob + b_ob) // 2

    above = mask_colour >= 255
    below = np.minimum(mask_colour + ob[:, :, np.newaxis] * (255 - mask_colour) // 256, 255)

    image_np = np.uint8(image)
    below[:, :, 3] = image_np[:, :, 3]
    mask_pal = np.uint8(mask)
    blended = np.where(np.broadcast_to((mask_pal == 0)[:, :, np.newaxis], (*mask_pal.shape, 4)), image_np, below)

    return Image.fromarray(blended.astype("uint8"))
