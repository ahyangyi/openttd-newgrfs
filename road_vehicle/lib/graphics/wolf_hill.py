import grf

wolf_default_road_vehicle_offsets = {
    6: ((0, 0), (-10, -11), (0, 0), (-5, -11), (0, 0), (-20, -11), (0, 0), (-18, -18)),
}
wolf_spritesheet_bounding_boxes = (
    (0, 1, 1),
    (0, 26, 24),
    (0, 1, 1),
    (34, 26, 24),
    (0, 1, 1),
    (68, 26, 24),
    (0, 1, 1),
    (102, 26, 24),
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


def wolf_hill_alternative_template(length, scales, path):
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
        if i % 2 == 1
        else grf.EMPTY_SPRITE
        for i in range(8)
    ]
