import pytest
from manapool.card import Card, UNKNOWN


def test_card_title_required():
    with pytest.raises(ValueError):
        Card(None)
    with pytest.raises(ValueError):
        Card("")


def test_card_constructor_mvid_defaults_unknown():
    c = Card("Riemann")
    assert (c.mvid == UNKNOWN)


def test_card_constructor_mvid_accepts_unknown_or_int():
    c = Card("Purphoros's Intervention", mvid=476402)
    assert (c.mvid == 476402)

    c = Card("Riemann", mvid=UNKNOWN)
    assert (c.mvid == UNKNOWN)

    with pytest.raises(ValueError):
        Card("Riemann", mvid="Euler")

    c = Card("Purphoros's Intervention", mvid="476402")
    assert (c.mvid == 476402)


def test_card_title_str_converts():
    c = Card(1)
    assert (c.title == "1")

    class Dummy:
        def __str__(self):
            return ""

    with pytest.raises(ValueError):
        Card(Dummy())
