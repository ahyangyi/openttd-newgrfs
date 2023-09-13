rebuild: clean all

all: road_vehicle.grf aegis.grf bridge.grf house.grf road.grf

rv: clean_rv road_vehicle.grf

rvf: clean_rv
	python3 -m road_vehicle.gen gen --fast

house: clean_house house.grf

road: clean_road road.grf

road_csv: road.csv

md: road_vehicle.md

bridge: clean_bridge bridge.grf

aegis: clean_aegis aegis.grf

clean_rv:
	rm -f road_vehicle.grf

clean_house:
	rm -f house.grf

clean_road:
	rm -f road.grf

clean_bridge:
	rm -f bridge.grf

clean_aegis:
	rm -f aegis.grf

clean:
	rm -f *.grf

road_vehicle.grf:
	python3 -m road_vehicle.gen gen

road_vehicle.md:
	python3 -m road_vehicle.gen print

doc.rv:
	python3 -m road_vehicle.gen doc

doc.rt:
	python3 -m road.dovemere_gen doc

doc.aegis:
	python3 -m industry.aegis_gen doc

aegis.grf:
	python3 -m industry.aegis_gen gen

bridge.grf:
	python3 -m bridge.dovemere_gen

house.grf:
	python3 -m house.dovemere_gen

road.grf:
	python3 -m road.dovemere_gen

road.csv:
	python3 -m road.dovemere_gen csv
