from industry.lib.industry import symmetrize


small_set = symmetrize(
    [
        (
            "xxx",
            "xxx",
            "xxx",
        ),
        (
            " xx ",
            "xxxx",
            "xxxx",
            " xx ",
        ),
        (
            " xx ",
            "xxxx",
            " xxx",
            "  x ",
        ),
        (
            " xxx",
            "xxxx",
            "xxxx",
            " xx ",
        ),
    ]
)
