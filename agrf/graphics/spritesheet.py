import grf
import math


def guess_dimens(width, height, angle, bbox):
    radian = math.radians(angle)
    cos, sin = math.cos(radian), math.sin(radian)

    x, y, z = bbox["x"], bbox["y"], bbox["z"]

    xcom, ycom = abs(x * cos), abs(y * sin)
    pxcom, pycom = abs(x * sin), abs(y * cos)

    horizontal_height = (xcom + ycom) * 0.5  # 30 deg

    if height == 0:
        ratio = (horizontal_height + z) / (pxcom + pycom)
        height_float = ratio * width
        height = math.ceil(height_float)

    real_ratio = (horizontal_height + z * 3**0.5 / 2) / (pxcom + pycom)
    real_height_float = real_ratio * width
    z = (z * 3**0.5 / 2) / (pxcom + pycom) * width

    delta = height - real_height_float

    return height, delta, z


deltas = [[0, -2], [2, -1], [4, 0], [2, 1], [0, 2], [-2, 1], [-4, 0], [-2, -1]]

scale_to_zoom = {1: grf.ZOOM_4X, 2: grf.ZOOM_2X, 4: grf.ZOOM_NORMAL}


def spritesheet_template(
    diff,
    path,
    dimens,
    angles,
    bbox,
    bbox_joggle=None,
    bpps=[8, 32],
    scales=[1, 2, 4],
    xdiff=0,
    ydiff=0,
    shift=0,
    road_mode=False,
):
    guessed_dimens = []
    for i in range(len(dimens)):
        x, y = dimens[i]
        y, z_ydiff, z_height = guess_dimens(x, y, angles[i], bbox)
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
        grf.AlternativeSprites(
            *(
                with_optional_mask(
                    grf.FileSprite(
                        grf.ImageFile(f"{path}_{scale}x_{bpp}bpp.png"),
                        (sum(guessed_dimens[j][0] for j in range(i)) + i * 8) * scale,
                        0,
                        guessed_dimens[i][0] * scale,
                        guessed_dimens[i][1] * scale,
                        xofs=get_rels(i, diff, scale)[0],
                        yofs=get_rels(i, diff, scale)[1],
                        bpp=bpp,
                        zoom=scale_to_zoom[scale],
                    ),
                    grf.FileSprite(
                        grf.ImageFile(f"{path}_{scale}x_mask.png"),
                        (sum(guessed_dimens[j][0] for j in range(i)) + i * 8) * scale,
                        0,
                        guessed_dimens[i][0] * scale,
                        guessed_dimens[i][1] * scale,
                    )
                    if bpp == 32
                    else None,
                )
                for bpp in bpps
                for scale in scales
            )
        )
        for idx in range(len(dimens))
        for i in [(idx + shift) % len(dimens)]
    ]
