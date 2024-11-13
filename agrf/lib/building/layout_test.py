from agrf.lib.building.layout import ADefaultGroundSprite


def test_default_groundsprite():
    gs1012 = ADefaultGroundSprite(1012)

    graphics = gs1012.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67
