from ..vehicles.buses import (
    happyone,
    rime,
    longriver,
    longriver_coach,
    longriver_articulated,
    longriver_2decker,
    raregem,
    milkyway_2decker,
)
from ..vehicles.lorries import freedom, freedom_mkii, shield, happyone as happyone_truck, yellowriver
from ..vehicles.debug import visible_serpent
from ..vehicles.monorail import nova
from road_vehicle.lib.roster import Roster

roster = Roster(
    happyone,
    rime,
    longriver,
    longriver_coach,
    longriver_articulated,
    longriver_2decker,
    raregem,
    milkyway_2decker,
    happyone_truck,
    freedom,
    freedom_mkii,
    shield,
    yellowriver,
    nova,
    visible_serpent,
)
