from . import load_font


def test_font():
    assert load_font("resources/AntaeusConsoleNumbers.otf", 12) is not None