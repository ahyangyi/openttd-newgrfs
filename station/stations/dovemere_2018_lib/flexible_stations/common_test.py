from station.stations.dovemere_2018_lib.flexible_stations.common import determine_platform_odd, determine_platform_even


def test_determine_platform_odd():
    assert "".join(determine_platform_odd(t, 8 - t) for t in range(1, 8)) == "nfdddnf"


def test_determine_platform_even():
    assert "".join(determine_platform_even(t, 8 - t) for t in range(1, 8)) == "fnfdnfn"
