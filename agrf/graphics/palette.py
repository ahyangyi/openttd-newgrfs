import json

with open("files/ttd_palette.json") as f:
    PALETTE = json.load(f)["entries"]


class CompanyColour:
    DARK_BLUE = 0xC6
    PALE_GREEN = 0x60
    PINK = 0x2A
    YELLOW = 0x3E
    RED = 0xB3
    LIGHT_BLUE = 0x9A
    GREEN = 0x52
    DARK_GREEN = 0x58
    BLUE = 0x92
    CREAM = 0x72
    MAUVE = 0x80
    PURPLE = 0x88
    ORANGE = 0x40
    BROWN = 0x20
    GREY = 0x4
    WHITE = 0x8
