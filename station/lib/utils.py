import inspect
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


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def globalize(self):
        # black magic supplied by ChatGPT, don't ask
        caller_module = inspect.currentframe().f_back.f_globals
        for k, v in self.items():
            caller_module[k] = v
