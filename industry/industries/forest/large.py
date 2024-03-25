from industry.lib.industry import symmetrize

large_set = symmetrize(
    [
        (" xxxx ", "xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx", " xxxx "),
        (" xxxx  ", "xxxxxx ", "xxxxxxx", "xxxxxxx", "xxxxxxx", "xxxxxxx", " xxxxx "),
        (" xxxx  ", "xxxxxx ", "xxxxxxx", "xxxxxxx", "xxxxxxx", " xxxxxx", "  xxxx "),
        (" xxxxx ", "xxxxxxx", "xxxxxxx", "xxxxxxx", "xxxxxxx", "xxxxxxx", " xxxxx "),
    ]
)
