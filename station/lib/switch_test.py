import grf
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

    def lookup(self, w, h, x, y, t):
        return self.v


def test_horizontal_switch():
    a = make_horizontal_switch(lambda l, r: MockValue(l * 0x100 + r * 0x10))
    assert 0x30 == a.lookup(4, 4, 0, 0)
    assert 0x120 == a.lookup(4, 4, 1, 0)
    assert 0x32 == a.T.lookup(4, 4, 0, 0)
    assert 0x301 == a.R.lookup(4, 4, 0, 0)


def test_switch_compression():
    a = make_horizontal_switch(lambda l, r: l)
    a = a.to_index(None)
    assert isinstance(a, grf.Switch)
    assert len(a._ranges) == 15
    assert all(isinstance(v.ref, int) for v in a._ranges)


def test_switch_compression_2():
    a = make_horizontal_switch(lambda l, r: r)
    a = a.to_index(None)
    assert isinstance(a, grf.Switch)
    assert len(a._ranges) == 15
    assert all(isinstance(v.ref, int) for v in a._ranges)


def test_switch_compression_3():
    a = make_horizontal_switch(lambda l, r: l ^ r)
    a = a.to_index(None)
    assert isinstance(a, grf.Switch)
    assert len(a._ranges) == 15
    assert all(isinstance(v.ref, grf.Switch) for v in a._ranges)
