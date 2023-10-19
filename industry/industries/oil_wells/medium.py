from industry.lib.industry import symmetrize


medium_set = symmetrize(
    [
        (
            "x  ",
            "x  ",
            "xxx",
        ),
        (
            "x  ",
            "xx ",
            " xx",
        ),
        (
            "x   ",
            "xx  ",
            "  xx",
        ),
        (
            " x  ",
            "xxx ",
            "   x",
        ),
        (
            " x  ",
            "x x ",
            "x  x",
        ),
        (
            "x   ",
            "x   ",
            "x xx",
        ),
    ]
)
