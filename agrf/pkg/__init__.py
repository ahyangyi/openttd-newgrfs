import io
import pkgutil
from PIL import Image


def load_third_party_image(path):
    content = pkgutil.get_data("agrf", path)
    f = io.BytesIO(content)
    return Image.open(f)
