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
    def __init__(self, *args, schema=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self.schema = schema

    @staticmethod
    def __tuple_to_str(t):
        return "_".join(a for a in t if a is not None and a != "")

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError as ke:
            if isinstance(key, str):
                for k in self.keys():
                    if isinstance(k, tuple) and self.__tuple_to_str(k) == key:
                        return self[k]
            raise ke

    def globalize(self, **kwargs):
        # black magic supplied by ChatGPT, don't ask
        caller_module = inspect.currentframe().f_back.f_globals
        for k, v in self.items():
            if isinstance(k, str):
                caller_module[k] = v
