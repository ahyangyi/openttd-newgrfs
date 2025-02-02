rebuild: clean all

all: road_vehicle.grf aegis.grf bridge.grf station.grf house.grf road.grf

rv: clean_rv road_vehicle.grf

rvf: clean_rv
	python3 -m road_vehicle.gen gen --fast

house: clean_house house.grf

road: clean_road road.grf

road_csv: road.csv

md: road_vehicle.md

bridge: clean_bridge bridge.grf

station: clean_station station.grf

aegis: clean_aegis aegis.grf

clean_rv:
	rm -f road_vehicle.grf

clean_house:
	rm -f house.grf

clean_road:
	rm -f road.grf

clean_bridge:
	rm -f bridge.grf

clean_station:
	rm -f station.grf

clean_aegis:
	rm -f aegis.grf

clean:
	rm -f *.grf

road_vehicle.grf:
	python3 -m road_vehicle.gen gen

road_vehicle.md:
	python3 -m road_vehicle.gen print

doc.bridge:
	python3 -m bridge.dovemere_gen doc

doc.station:
	python3 -m station.dovemere_gen doc

doc.rv:
	python3 -m road_vehicle.gen doc

doc.rt:
	python3 -m road.dovemere_gen doc

doc.aegis:
	python3 -m industry.aegis_gen doc

doc.house:
	python3 -m house.dovemere_gen doc

test.aegis:
	python3 -m industry.aegis_gen test

aegis.grf:
	python3 -m industry.aegis_gen gen

bridge.grf:
	python3 -m bridge.dovemere_gen gen

station.grf:
	python3 -m station.dovemere_gen gen

house.grf:
	python3 -m house.dovemere_gen gen

road.grf:
	python3 -m road.dovemere_gen gen

road.csv:
	python3 -m road.dovemere_gen csv

profile.aegis:
	python3 -m cProfile -o .prof/aegis_gen.prof -m industry.aegis_gen gen
	gprof2dot -f pstats .prof/aegis_gen.prof | dot -Tpng -o .prof/aegis_gen_prof.png

profile.station:
	python3 -m cProfile -o .prof/station_gen.prof -m station.dovemere_gen gen
	gprof2dot -f pstats .prof/station_gen.prof | dot -Tpng -o .prof/station_gen_prof.png
