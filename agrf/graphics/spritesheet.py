import grf
import math


def guess_dimens(width, angle, bbox):
    radian = math.radians(angle)
    cos, sin = math.cos(radian), math.sin(radian)

    x, y, z = bbox["x"], bbox["y"], bbox["z"]

    xcom, ycom = abs(x * cos), abs(y * sin)
    pxcom, pycom = abs(x * sin), abs(y * cos)

    horizontal_height = (xcom + ycom) * 0.5  # 30 deg

    # XXX: formula doesn't make sense, but is how gorender works
    ratio = (horizontal_height + z) / (pxcom + pycom)
    height_float = ratio * width

    height = math.ceil(height_float)
    delta = height - height_float

    return height, delta


deltas = [
    [0, -2],
    [2, -1],
    [4, 0],
    [2, 1],
    [0, 2],
    [-2, 1],
    [-4, 0],
    [-2, -1],
]

scale_to_zoom = {
    1: grf.ZOOM_4X,
    2: grf.ZOOM_2X,
    4: grf.ZOOM_NORMAL,
}


def spritesheet_template(diff, path, dimens, bbox, bbox_joggle=None, bpps=[8, 32], scales=[1, 2, 4], ydiff=0, shift=0):
    guessed_dimens = []
    for i in range(8):
        x, y = dimens[i]
        if y == 0:
            y, _ = guess_dimens(x, i * 45, bbox)
        guessed_dimens.append((x, y))

    def get_rels(direction, diff, scale):
        w, h = guessed_dimens[direction][0] * scale, guessed_dimens[direction][1] * scale
        xrel = -w / 2
        yrel = -h / 2

        yrel -= 2 * scale
        yrel += ydiff * scale

        xrel += deltas[direction][0] * diff * scale
        yrel += deltas[direction][1] * diff * scale

        if bbox_joggle is not None:
            xrel += bbox_joggle[direction][0] * scale
            yrel += bbox_joggle[direction][1] * scale

        return int(xrel + 0.5), int(yrel + 0.5)

    return [
        grf.AlternativeSprites(
            *(
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
                    mask=grf.FileMask(
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
        for idx in range(8)
        for i in [(idx + shift) % 8]
    ]
