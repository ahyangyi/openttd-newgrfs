import grf
import numpy as np
from PIL import Image
from station.lib import Registers
from agrf.lib.building.layout import AGroundSprite, ADefaultGroundSprite, AParentSprite, AChildSprite, ALayout
from agrf.lib.building.symmetry import BuildingSymmetrical
from agrf.lib.building.image_sprite import image_sprite
from agrf.graphics.misc import SCALE_TO_ZOOM

temperate_1011 = np.array(Image.open("agrf/third_party/opengfx2/temperate/1011.png"))
temperate_1012 = np.array(Image.open("agrf/third_party/opengfx2/temperate/1012.png"))
temperate_1011_over_1012 = np.array(
    Image.alpha_composite(Image.fromarray(temperate_1012), Image.fromarray(temperate_1011))
)


dgs1012 = ADefaultGroundSprite(1012)
gs1012 = AGroundSprite(image_sprite("agrf/third_party/opengfx2/temperate/1012.png"))
ps1012 = AParentSprite(image_sprite("agrf/third_party/opengfx2/temperate/1012.png"), (16, 16, 1), (0, 0, 0))
ch1011snow = AChildSprite(
    image_sprite("agrf/third_party/opengfx2/temperate/1011.png"), (0, 0), flags={"dodraw": Registers.SNOW}
)
l1012 = ALayout(dgs1012, [], True)
l1012snow = ALayout(gs1012 + ch1011snow, [], True)


def test_default_groundsprite():
    assert (temperate_1012 == dgs1012.graphics(4, 32).to_image()).all()


def test_default_groundsprite_M():
    assert (temperate_1011 == dgs1012.M.graphics(4, 32).to_image()).all()


def test_default_groundsprite_R():
    assert (temperate_1012 == dgs1012.R.graphics(4, 32).to_image()).all()


def test_default_groundsprite_T():
    assert (temperate_1012 == dgs1012.T.graphics(4, 32).to_image()).all()


def test_groundsprite():
    assert (temperate_1012 == gs1012.graphics(4, 32).to_image()).all()


def test_parentsprite():
    assert (temperate_1012 == ps1012.graphics(4, 32).to_image()).all()


def test_layout():
    assert (temperate_1012 == l1012.graphics(4, 32).to_image()).all()


def test_layout_M():
    assert (temperate_1011 == l1012.M.graphics(4, 32).to_image()).all()


def test_layout_R():
    assert (temperate_1012 == l1012.R.graphics(4, 32).to_image()).all()


def test_layout_T():
    assert (temperate_1012 == l1012.T.graphics(4, 32).to_image()).all()


def test_default_ground_sprite_to_parentsprite():
    # For now, just make sure this can run
    dgs1012.to_parentsprite()


def test_layout_snow():
    assert (temperate_1012 == l1012snow.graphics(4, 32).to_image()).all()


def test_layout_snow_arctic():
    assert (temperate_1011_over_1012 == l1012snow.graphics(4, 32, climate="arctic", subclimate="snow").to_image()).all()


def test_ground_sprite_to_parentsprite():
    # For now, just make sure this can run
    gs1012.to_parentsprite()


def test_pushdown():
    # FIXME also examine the offsets
    assert (temperate_1012 == ps1012.pushdown(1).graphics(4, 32).to_image()).all()


def test_symmetry():
    gs1012 = ADefaultGroundSprite(1012)
    gs1011 = ADefaultGroundSprite(1011)

    g = BuildingSymmetrical.create_variants([gs1012, gs1011])
    assert g is g.R
    assert g is g.T
    assert g is g.M.M
