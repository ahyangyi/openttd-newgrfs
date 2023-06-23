from house.lib import AHouse
from pygorender import Config, render

import grf

render(
    Config("house/files/gorender.json"),
    "house/voxels/dovemere_gable.vox",
    output_path="house/voxels/render/dovemere_gable/render",
)

scale_to_zoom = {
    1: grf.ZOOM_4X,
    2: grf.ZOOM_2X,
    4: grf.ZOOM_NORMAL,
}


def template(path):
    return [
        grf.AlternativeSprites(
            *(
                grf.FileSprite(
                    grf.ImageFile(f"{path}_{scale}x_{bpp}bpp.png"),
                    72 * scale * i,
                    0,
                    64 * scale,
                    78 * scale,
                    xofs=int((-32 + 1.5) * scale),
                    yofs=int((-48 + 2.5) * scale),
                    bpp=bpp,
                    zoom=scale_to_zoom[scale],
                    mask=grf.FileMask(
                        grf.ImageFile(f"{path}_{scale}x_mask.png"),
                        72 * scale * i,
                        0,
                        64 * scale,
                        78 * scale,
                    )
                    if bpp == 32
                    else None,
                )
                for bpp in [8, 32]
                for scale in [1, 2, 4]
            )
        )
        for i in range(1)
    ]


the_house = AHouse(
    id=0x80,
    name="House",
    sprites=template("house/voxels/render/dovemere_gable/render"),
    flags=0x1,
    availability_mask=0xF81F,
)
