import grf
from agrf.lib.building.layout import AGroundSprite, ADefaultGroundSprite, ALayout
from agrf.lib.building.symmetry import BuildingSymmetrical
from agrf.lib.building.image_sprite import image_sprite
from agrf.graphics.misc import SCALE_TO_ZOOM


def test_default_groundsprite():
    gs1012 = ADefaultGroundSprite(1012)

    graphics = gs1012.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67

    m_graphics = gs1012.M.graphics(4, 32).to_image()
    assert m_graphics.shape == (127, 256, 4)
    assert m_graphics[64, 128, 1] == 72

    r_graphics = gs1012.R.graphics(4, 32).to_image()
    assert r_graphics.shape == (127, 256, 4)
    assert r_graphics[64, 128, 1] == 67

    t_graphics = gs1012.T.graphics(4, 32).to_image()
    assert t_graphics.shape == (127, 256, 4)
    assert t_graphics[64, 128, 1] == 67


def test_groundsprite():
    gs1012 = AGroundSprite(image_sprite("agrf/third_party/opengfx2/temperate/1012.png"))
    graphics = gs1012.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67


def test_layout():
    gs1012 = ADefaultGroundSprite(1012)
    l = ALayout(gs1012, [], True)

    graphics = l.graphics(4, 32).to_image()
    assert graphics.shape == (127, 256, 4)
    assert graphics[64, 128, 1] == 67

    m_graphics = l.M.graphics(4, 32).to_image()
    assert m_graphics.shape == (127, 256, 4)
    assert m_graphics[64, 128, 1] == 72

    r_graphics = l.R.graphics(4, 32).to_image()
    assert r_graphics.shape == (127, 256, 4)
    assert r_graphics[64, 128, 1] == 67

    t_graphics = l.T.graphics(4, 32).to_image()
    assert t_graphics.shape == (127, 256, 4)
    assert t_graphics[64, 128, 1] == 67


def test_symmetry():
    gs1012 = ADefaultGroundSprite(1012)
    gs1011 = ADefaultGroundSprite(1011)

    g = BuildingSymmetrical.create_variants([gs1012, gs1011])
    assert g is g.R
    assert g is g.T
    assert g is g.M.M
