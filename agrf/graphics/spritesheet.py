import grf
import math
from .misc import SCALE_TO_ZOOM


__image_file_cache = {}


def make_image_file(path):
    if path in __image_file_cache:
        return __image_file_cache[path]
    __image_file_cache[path] = grf.ImageFile(path)
    return __image_file_cache[path]


def guess_dimens(width, height, angle, bbox, z_scale):
    radian = math.radians(angle)
    cos, sin = math.cos(radian), math.sin(radian)

    x, y, z = bbox["x"], bbox["y"], bbox["z"] * z_scale

    xcom, ycom = abs(x * cos), abs(y * sin)
    pxcom, pycom = abs(x * sin), abs(y * cos)

    horizontal_height = (xcom + ycom) * 0.5

    if height == 0:
        ratio = (horizontal_height + z) / (pxcom + pycom)
        height_float = ratio * width
        height = math.ceil(height_float)

    real_ratio = (horizontal_height + z) / (pxcom + pycom)
    real_height_float = real_ratio * width
    z = z / (pxcom + pycom) * width

    delta = height - real_height_float

    return height, delta, z


class LazyAlternativeSprites(grf.AlternativeSprites):
    def __init__(self, voxel, part, *sprites):
        super().__init__(*sprites)
        self.voxel = voxel
        self.part = part

    def get_sprite(self, *, zoom=None, bpp=None):
        self.voxel.render()
        return super().get_sprite(zoom=zoom, bpp=bpp)

    def get_fingerprint(self):
        return {"name": self.voxel.name, "part": self.part, "prefix": self.voxel.prefix}

    def get_resources(self):
        self.voxel.render()
        return super().get_resources()

    def get_resource_files(self):
        self.voxel.render()
        return super().get_resource_files()

    def __repr__(self):
        return f"LazyAlternativeSprites<{self.voxel.name}:{self.part}>"


def spritesheet_template(
    voxel,
    diff,
    path,
    dimens,
    angles,
    bbox,
    deltas,
    z_scale,
    bbox_joggle=None,
    bpps=(8, 32),
    scales=(1, 2, 4),
    xdiff=0,
    ydiff=0,
    shift=0,
    road_mode=False,
):
    guessed_dimens = []
    for i in range(len(dimens)):
        x, y = dimens[i]
        y, z_ydiff, z_height = guess_dimens(x, y, angles[i], bbox, z_scale)
        guessed_dimens.append((x, y, z_ydiff, z_height))

    def get_rels(direction, diff, scale):
        w, h, z_ydiff, z_height = map(lambda a: a * scale, guessed_dimens[direction])
        xrel = -w / 2
        if road_mode:
            yrel = -z_height
        else:
            yrel = -h / 2

        xrel += xdiff * scale
        yrel += ydiff * scale
        yrel -= z_ydiff

        if diff != 0:
            xrel += deltas[direction][0] * diff * scale
            yrel += deltas[direction][1] * diff * scale

        if bbox_joggle is not None:
            xrel += bbox_joggle[direction][0] * scale
            yrel += bbox_joggle[direction][1] * scale

        return int(xrel + 0.5), int(yrel + 0.5)

    def with_optional_mask(sprite, mask):
        if mask is None:
            return sprite
        return grf.WithMask(sprite, mask)

    return [
        LazyAlternativeSprites(
            voxel,
            idx,
            *(
                with_optional_mask(
                    grf.FileSprite(
                        make_image_file(f"{path}_{scale}x_{bpp}bpp.png"),
                        (sum(guessed_dimens[j][0] for j in range(i)) + i * 8) * scale,
                        0,
                        guessed_dimens[i][0] * scale,
                        guessed_dimens[i][1] * scale,
                        xofs=get_rels(i, diff, scale)[0],
                        yofs=get_rels(i, diff, scale)[1],
                        bpp=bpp,
                        zoom=SCALE_TO_ZOOM[scale],
                    ),
                    (
                        grf.FileSprite(
                            make_image_file(f"{path}_{scale}x_mask.png"),
                            (sum(guessed_dimens[j][0] for j in range(i)) + i * 8) * scale,
                            0,
                            guessed_dimens[i][0] * scale,
                            guessed_dimens[i][1] * scale,
                        )
                        if bpp == 32
                        else None
                    ),
                )
                for bpp in bpps
                for scale in scales
            ),
        )
        for idx in range(len(dimens))
        for i in [(idx + shift) % len(dimens)]
    ]
