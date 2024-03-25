from industry.lib.industry import symmetrize


huge_set = symmetrize(
    [
        ("x       ", "  x     ", "x    x  ", "        ", "x  x    ", " x   x  ", "      xx"),
        (" x      ", "x     x ", "x    x x", "    x   ", "    x   ", "   x    ", "  x     "),
    ]
)
