rebuild: clean all

all: road_vehicle.grf aegis.grf bridge.grf house.grf road.grf

rv: clean_rv road_vehicle.grf

rvf: clean_rv
	python3 -m road_vehicle.gen gen --fast

house: clean_house house.grf

md: road_vehicle.md

clean_rv:
	rm -f road_vehicle.grf

clean_house:
	rm -f house.grf

clean:
	rm -f *.grf

road_vehicle.grf:
	python3 -m road_vehicle.gen gen

road_vehicle.md:
	python3 -m road_vehicle.gen print

aegis.grf:
	python3 -m industry.aegis_gen

bridge.grf:
	python3 -m bridge.dovemere_gen

house.grf:
	python3 -m house.dovemere_gen

road.grf:
	python3 -m road.dovemere_gen
