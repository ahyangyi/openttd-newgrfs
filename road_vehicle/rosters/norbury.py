from ..vehicles.buses import northwing, northwing_articulated, joyfield, joyfield_articulated
from ..vehicles.lorries import freedom, freedom_mkii, shield, leeway as leeway_truck, yellowriver
from ..vehicles.trolleybuses import burger
from road_vehicle.lib.roster import Roster

the_roster = Roster(
    "NORBURY",
    northwing,
    northwing_articulated,
    joyfield,
    joyfield_articulated,
    leeway_truck,
    freedom,
    freedom_mkii,
    shield,
    yellowriver,
    burger,
)
