from station.stations.dovemere_2018_lib.flexible_stations.common import (
    determine_platform_odd,
    determine_platform_even,
    get_left_index_suffix,
    named_tiles,
)


def check_platform_function(fn, n, expected):
    assert expected == "".join(fn(min(t, 15), min(n - 1 - t, 15)) for t in range(n))


def test_determine_platform_odd():
    check_platform_function(determine_platform_odd, 7, "nfndfnf")
    check_platform_function(determine_platform_odd, 8, "nfnfnfnf")
    check_platform_function(determine_platform_odd, 9, "nfndddfnf")
    check_platform_function(determine_platform_odd, 10, "nfnfnfnfnf")


def test_determine_platform_odd_huge():
    check_platform_function(determine_platform_odd, 29, "nf" * 6 + "ndddf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 30, "nf" * 6 + "nddddf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 31, "nf" * 6 + "ndddddf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 32, "nf" * 6 + "nddddddf" + "nf" * 6)
    check_platform_function(determine_platform_odd, 33, "nf" * 6 + "ndddddddf" + "nf" * 6)


def test_determine_platform_even():
    check_platform_function(determine_platform_even, 7, "fndddfn")
    check_platform_function(determine_platform_even, 8, "fnfnfnfn")
    check_platform_function(determine_platform_even, 9, "fnfndfnfn")
    check_platform_function(determine_platform_even, 10, "fnfnfnfnfn")


def test_determine_platform_even_huge():
    check_platform_function(determine_platform_even, 29, "fn" * 7 + "d" + "fn" * 7)
    check_platform_function(determine_platform_even, 30, "fn" * 7 + "dd" + "fn" * 7)
    check_platform_function(determine_platform_even, 31, "fn" * 7 + "ddd" + "fn" * 7)
    check_platform_function(determine_platform_even, 32, "fn" * 7 + "dddd" + "fn" * 7)
    check_platform_function(determine_platform_even, 33, "fn" * 7 + "ddddd" + "fn" * 7)


def test_get_left_index_suffix():
    f = ("concrete", "shelter_1", "f")
    n = ("concrete", "shelter_1", "n")

    assert named_tiles.side_a_concrete_shelter_1_f is get_left_index_suffix(3, 1, f)
    assert named_tiles.side_b2_concrete_shelter_1_n.T is get_left_index_suffix(2, 2, f)
    assert named_tiles.side_a_concrete_shelter_1_n.T is get_left_index_suffix(1, 3, f)

    assert named_tiles.side_a_concrete_shelter_1_n is get_left_index_suffix(4, 1, n)
    assert named_tiles.side_b_concrete_shelter_1_n is get_left_index_suffix(3, 2, n)
    assert named_tiles.side_b_concrete_shelter_1_f.T is get_left_index_suffix(2, 3, n)
    assert named_tiles.side_a_concrete_shelter_1_f.T is get_left_index_suffix(1, 4, n)
