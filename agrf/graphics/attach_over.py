from PIL import Image, ImageChops
import numpy as np


# alpha blend image 1 over image 2, w/ offset
def attach_over(image1, mask1, image2, mask2, offset):
    image1 = np.uint8(image1)
    image2 = np.uint8(image2)
    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]
    ox, oy = offset

    if ox < 0:
        o1x = -ox
        o2x = 0
        w = max(w1 + o1x, w2)
    else:
        o1x = 0
        o2x = ox
        w = max(w1, w2 + o2x)

    if oy < 0:
        o1y = -oy
        o2y = 0
        h = max(h1 + o1y, h2)
    else:
        o1y = 0
        o2y = oy
        h = max(h1, h2 + o2y)

    new_image = np.zeros((h, w, 4), dtype=np.uint8)
    new_image[o1y : o1y + h1, o1x : o1x + w1, :] = image1
    blend_port = new_image[o2y : o2y + h2, o2x : o2x + w2, :]

    alpha1 = blend_port[:, :, 3:].astype(np.uint32)
    alpha2 = image2[:, :, 3:].astype(np.uint32)
    new_alpha = alpha1 * 255 + alpha2 * (255 - alpha1)
    new_rgb = (
        alpha1 * 255 * blend_port[:, :, :3] + alpha2 * (255 - alpha1) * image2[:, :, :3] + new_alpha // 2
    ) // np.maximum(new_alpha, 1)
    blend_port[:, :, :3] = new_rgb
    blend_port[:, :, 3:] = (new_alpha + 128) // 255
    new_image = Image.fromarray(new_image)

    new_mask = np.zeros((h, w), dtype=np.uint8)
    new_mask[o1y : o1y + h1, o1x : o1x + w1] = mask1
    blend_port = new_mask[o2y : o2y + h2, o2x : o2x + w2]
    transparency = blend_port == 0
    blend_port[:, :] = transparency * mask2 + (1 - transparency) * blend_port
    new_mask = Image.fromarray(new_mask, mode="P")
    new_mask.putpalette(mask1.getpalette())

    return new_image, new_mask
