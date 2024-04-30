from station.stations.dovemere_2018_lib.flexible_stations.common import (
    determine_platform_odd,
    determine_platform_even,
    get_left_index_suffix,
    named_tiles,
)


def check_platform_function(fn, n, expected):
    assert expected == "".join(fn(t, n - 1 - t) for t in range(n))


def test_determine_platform_odd():
    check_platform_function(determine_platform_odd, 7, "nfndfnf")
    check_platform_function(determine_platform_odd, 8, "nfnfnfnf")
    check_platform_function(determine_platform_odd, 9, "nfndddfnf")
    check_platform_function(determine_platform_odd, 10, "nfnfnfnfnf")


def test_determine_platform_even():
    check_platform_function(determine_platform_even, 7, "fndddfn")
    check_platform_function(determine_platform_even, 8, "fnfnfnfn")
    check_platform_function(determine_platform_even, 9, "fnfndfnfn")
    check_platform_function(determine_platform_even, 10, "fnfnfnfnfn")


def test_get_left_index_suffix():
    assert named_tiles.side_a_f is get_left_index_suffix(3, 1, "f")
    assert named_tiles.side_a2_n.T is get_left_index_suffix(2, 2, "f")
    assert named_tiles.side_a_f.T is get_left_index_suffix(1, 3, "f")
