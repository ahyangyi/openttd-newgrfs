from station.stations.dovemere_2018_lib.flexible_stations.common import determine_platform_odd, determine_platform_even


def check_platform_function(fn, n, expected):
    assert expected == "".join(fn(t, n - 1 - t) for t in range(1, n - 1))


def test_determine_platform_odd():
    check_platform_function(determine_platform_odd, 7, "nfdnf")
    check_platform_function(determine_platform_odd, 8, "nfnfnf")
    check_platform_function(determine_platform_odd, 9, "nfdddnf")
    check_platform_function(determine_platform_odd, 10, "nfnfnfnf")


def test_determine_platform_even():
    check_platform_function(determine_platform_even, 7, "fdddn")
    check_platform_function(determine_platform_even, 8, "fnfnfn")
    check_platform_function(determine_platform_even, 9, "fnfdnfn")
    check_platform_function(determine_platform_even, 10, "fnfnfnfn")
