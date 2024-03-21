from ..vehicles.buses import (
    happyone,
    rime,
    southwing_articulated,
    longriver,
    longriver_coach,
    longriver_articulated,
    longriver_2decker,
    raregem,
    milkyway_2decker,
    milkyway_coach,
)
from ..vehicles.lorries import freedom, freedom_mkii, shield, happyone as happyone_truck, yellowriver
from ..vehicles.monorail import nova
from road_vehicle.lib.roster import Roster

the_roster = Roster(
    "DOVEMERE",
    happyone,
    rime,
    southwing_articulated,
    longriver,
    longriver_coach,
    longriver_articulated,
    longriver_2decker,
    raregem,
    milkyway_2decker,
    milkyway_coach,
    happyone_truck,
    freedom,
    freedom_mkii,
    shield,
    yellowriver,
    nova,
)
