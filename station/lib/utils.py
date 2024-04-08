from agrf.graphics.palette import company_colour_remap


def get_1cc_remap(colour):
    return company_colour_remap(colour, colour).to_sprite()


def class_label_printable(x):
    ret = []
    for byte in x:
        if 0x20 <= byte <= 0x7F:
            ret.append(chr(byte))
        else:
            ret.append(hex(byte)[2:].upper())
    return "".join(ret)
