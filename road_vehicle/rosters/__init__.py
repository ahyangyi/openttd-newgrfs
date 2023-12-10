from road_vehicle.lib.roster import Roster
from . import dovemere, norbury

city_rosters = [x.the_roster for x in (dovemere, norbury)]

everything = Roster("EVERYTHING", *set(v for r in city_rosters for v in r.entries))

all_rosters = [everything] + city_rosters
