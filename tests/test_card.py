import pytest
from manapool.card import Card, UNKNOWN, ManaCost, Colour


# CARD TESTS

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


# MANACOST TESTS

def test_manacost_constructor_dict_of_colors():
    cost = ManaCost({Colour.Black: 1, Colour.Generic: 4})

    assert (cost.black == 1)
    assert (cost.generic == 4)
    for c in (col for col in Colour if col not in [Colour.Black, Colour.Generic]):
        assert (cost[c] == 0)

    cost = ManaCost({c: 1 for c in Colour.pure()})
    for c in Colour.pure():
        assert (cost[c] == 1)

    with pytest.raises(ValueError):
        cost = ManaCost({Colour.Red: 1, Colour.Blue: -1})
    with pytest.raises(ValueError):
        cost = ManaCost({Colour.Red: 1, Colour.Blue: "Euler"})


def test_manacost_constructor_none_values():
    with pytest.raises(ValueError):
        cost = ManaCost(None)


def test_manacost_converted():
    cost = ManaCost({Colour.Black: 1, Colour.Generic: 4})
    assert (cost.converted == 5)

    cost = ManaCost({c: 1 for c in Colour.pure()})
    assert (cost.converted == 5)

    cost = ManaCost()
    assert (cost.converted == 0)


def test_manacost_equality():
    cost1 = ManaCost({Colour.Black: 1, Colour.Generic: 4})
    cost2 = ManaCost({c: 1 for c in Colour.pure()})
    cost3 = ManaCost({Colour.Black: 1, Colour.Generic: 4})

    assert (cost1 != cost2)
    assert (cost1 == cost1)
    assert (cost3 == cost1)

    with pytest.raises(TypeError):
        assert (cost1 == "Riemann")
