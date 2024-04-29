from .switch import make_horizontal_switch


class MockValue:
    def __init__(self, v):
        self.v = v

    @property
    def T(self):
        return MockValue(self.v ^ 2)

    @property
    def R(self):
        return MockValue(self.v ^ 1)

    def lookup(self, w, h, x, y):
        return self.v


def test_horizontal_switch():
    a = make_horizontal_switch(lambda l, r: MockValue(l * 0x100 + r * 0x10))
    assert 0x30 == a.lookup(4, 4, 0, 0)
