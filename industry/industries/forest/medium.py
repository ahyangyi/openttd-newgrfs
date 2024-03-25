from industry.lib.industry import symmetrize

medium_set = symmetrize(
    [
        ("xxxx", "xxxx", "xxxx", "xxxx", " xx "),
        ("xxxx", "xxxx", "xxxx", "xxxx", "xxxx", " xx "),
        (" xxxx ", "xxxxxx", "xxxxxx", " xxxx "),
        (" xxx ", "xxxxx", "xxxxx", "xxxxx", " xxx "),
        (" xxx ", "xxxxx", "xxxxx", "xxxxx", "xxxxx", " xxx "),
        ("xxxxx", "xxxxx", "xxxxx", "xxxxx", " xxx "),
        ("xxxxx", "xxxxx", "xxxxx", "xxxxx", "xxxxx", " xxx "),
    ]
)
