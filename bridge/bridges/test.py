from bridge.lib import ABridge
from datetime import date
import grf


the_bridge = ABridge(
    id=0x01,
    name="Test Bridge",
    front=None,
    back=None,
    pillar=None,
    intro_year_since_1920=0,
    purchase_text="Build Test Bridge",
    description_rail="Test Bridge (rail)",
    description_road="Test Bridge (road)",
)
