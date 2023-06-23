import grf

wolf_default_road_vehicle_offsets = {
    1: ((-3, -25), (-8, -16), (-4, -14), (-3, -11), (-4, -11), (-22, -8), (-32, -8), (-17, -16)),
    2: ((-3, -24), (-9, -16), (-6, -14), (-4, -11), (-4, -12), (-21, -9), (-30, -8), (-16, -16)),
    3: ((-3, -23), (-10, -15), (-8, -14), (-5, -11), (-4, -13), (-20, -9), (-28, -8), (-15, -15)),
    4: ((-3, -22), (-11, -15), (-10, -14), (-6, -11), (-4, -14), (-19, -10), (-26, -8), (-14, -15)),
    5: ((-3, -21), (-12, -14), (-12, -14), (-7, -11), (-4, -15), (-18, -10), (-24, -8), (-13, -14)),
    6: ((-3, -20), (-13, -14), (-14, -14), (-8, -11), (-4, -16), (-17, -11), (-22, -8), (-12, -14)),
    7: ((-3, -19), (-14, -13), (-16, -14), (-9, -11), (-4, -17), (-16, -11), (-20, -8), (-11, -13)),
    8: ((-3, -18), (-15, -13), (-18, -14), (-10, -11), (-4, -18), (-15, -12), (-18, -8), (-10, -13)),
}
wolf_spritesheet_bounding_boxes = (
    (0, 9, 32),
    (17, 26, 24),
    (51, 36, 14),
    (95, 26, 24),
    (129, 9, 32),
    (146, 26, 24),
    (180, 36, 14),
    (224, 26, 24),
)


def wolf_template(length, scale, func):
    return [
        func(
            wolf_spritesheet_bounding_boxes[i][0] * scale,
            0,
            wolf_spritesheet_bounding_boxes[i][1] * scale,
            wolf_spritesheet_bounding_boxes[i][2] * scale,
            xofs=wolf_default_road_vehicle_offsets[length][i][0] * scale,
            yofs=wolf_default_road_vehicle_offsets[length][i][1] * scale - scale // 2,
        )
        for i in range(8)
    ]


scale_to_zoom = {
    1: grf.ZOOM_4X,
    2: grf.ZOOM_2X,
    4: grf.ZOOM_NORMAL,
}


def wolf_alternative_template(length, scales, path):
    return [
        grf.AlternativeSprites(
            *(
                grf.FileSprite(
                    grf.ImageFile(f"{path}_{scale}x_{bpp}bpp.png"),
                    wolf_spritesheet_bounding_boxes[i][0] * scale,
                    0,
                    wolf_spritesheet_bounding_boxes[i][1] * scale,
                    wolf_spritesheet_bounding_boxes[i][2] * scale,
                    xofs=wolf_default_road_vehicle_offsets[length][i][0] * scale,
                    yofs=wolf_default_road_vehicle_offsets[length][i][1] * scale - scale // 2,
                    bpp=bpp,
                    zoom=scale_to_zoom[scale],
                    mask=(grf.ImageFile(f"{path}_{scale}x_mask.png"), 0, 0) if bpp == 32 else None,
                )
                for bpp in [8, 32]
                for scale in [1, 2, 4]
            )
        )
        for i in range(8)
    ]
