from industry.lib.industry import symmetrize


large_set = symmetrize(
    [
        (
            "x     ",
            "x     ",
            "x     ",
            " x    ",
            "   xxx",
        ),
        (
            " x    ",
            "x    x",
            "    x ",
            "    x ",
            "  xx  ",
        ),
    ]
)
