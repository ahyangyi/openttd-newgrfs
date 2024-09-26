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
    def __init__(self, *args, prefix=None, schema=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self._prefix = prefix
        self._schema = schema

    @staticmethod
    def __tuple_to_str(t):
        return "_".join(a for a in t if a is not None and a != "")

    def __contains__(self, item):
        if super().__contains__(item):
            return True
        if isinstance(item, tuple):
            # XXX Slow
            for k, v in self.items():
                if all((a is None or b is None or a == b) for a, b in zip(k, item)):
                    return True
        return False

    def __getitem__(self, item):
        if super().__contains__(item):
            return super().__getitem__(item)
        if isinstance(item, tuple):
            # XXX Slow
            for k, v in self.items():
                if all((a is None or b is None or a == b) for a, b in zip(k, item)):
                    return v
        raise KeyError(item)

    def populate(self):
        for k in list(self.keys()):
            if isinstance(k, tuple):
                str_key = self.__tuple_to_str(k)
                assert str_key not in self, f"populate() conflict! {str_key}"
                self[str_key] = self[k]

    def globalize(self, **kwargs):
        # black magic supplied by ChatGPT, don't ask
        caller_module = inspect.currentframe().f_back.f_globals

        for k, v in self.items():
            if isinstance(k, str) and len(kwargs) == 0:
                caller_module[k] = v
            elif isinstance(k, tuple):
                if all((kwargs.get(b) is None or a == kwargs.get(b)) for a, b in zip(k, self._schema)):
                    caller_module[
                        self.__tuple_to_str(
                            [self._prefix] + [a for a, b in zip(k, self._schema) if kwargs.get(b) is None]
                        )
                    ] = v
