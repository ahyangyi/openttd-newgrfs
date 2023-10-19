from industry.lib.industry import symmetrize


large_set = symmetrize(
    [
        (
            "x    ",
            "x    ",
            "xx   ",
            "  xxx",
        ),
        (
            "xx   ",
            "x  xx",
            "   x ",
            "  x  ",
        ),
    ]
)
