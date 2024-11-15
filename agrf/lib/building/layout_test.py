from agrf.lib.building.layout import ADefaultGroundSprite, ALayout


def test_default_groundsprite():
    gs1012 = ADefaultGroundSprite(1012)

    graphics = gs1012.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67

    m_graphics = gs1012.M.graphics(4, 32).to_image()
    assert m_graphics.shape == (127, 256, 4)
    assert m_graphics[64, 128, 1] == 72


def test_layout():
    gs1012 = ADefaultGroundSprite(1012)
    l = ALayout(gs1012, [], True)

    graphics = l.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67

    m_graphics = l.M.graphics(4, 32).to_image()
    assert m_graphics.shape == (127, 256, 4)
    assert m_graphics[64, 128, 1] == 72
