import pytest
from manapool.card import Card, UNKNOWN, ManaCost, Colour
import itertools


# CARD TESTS

def test_card_title_required():
    with pytest.raises(ValueError):
        Card(None)
    with pytest.raises(ValueError):
        Card("")


def test_card_constructor_mvid_defaults_unknown():
    c = Card("Riemann")
    assert (c.mvid == UNKNOWN)


def test_card_constructor_cost_defaults_unknown():
    c = Card("Riemann")
    assert (c.cost == UNKNOWN)


def test_card_constructor_mvid_accepts_unknown_or_int():
    c = Card("Purphoros's Intervention", mvid=476402)
    assert (c.mvid == 476402)

    c = Card("Riemann", mvid=UNKNOWN)
    assert (c.mvid == UNKNOWN)

    with pytest.raises(ValueError):
        Card("Riemann", mvid="Euler")

    c = Card("Purphoros's Intervention", mvid="476402")
    assert (c.mvid == 476402)


def test_card_constructor_cost_accepts_unknown_or_manacost():
    cost = ManaCost({Colour.Blue: 2})
    c = Card("Purphoros's Intervention", cost=cost)
    assert (c.cost == cost)

    c = Card("Riemann", cost=UNKNOWN)
    assert (c.cost == UNKNOWN)

    with pytest.raises(ValueError):
        Card("Riemann", cost="Euler")


def test_card_title_str_converts():
    c = Card(1)
    assert (c.title == "1")

    class Dummy:
        def __str__(self):
            return ""

    with pytest.raises(ValueError):
        Card(Dummy())


def test_card_equality():
    a = Card("Riemann")
    b = Card("Riemann")
    assert (a == b)

    b = Card("Euler")
    assert (a != b)

    b = Card("Riemann", mvid=123)
    assert (a != b)

    a = Card("Riemann", mvid=123)
    assert (a == b)

    a = Card("Riemann")
    b = Card("Riemann", cost=ManaCost({Colour.Blue: 2}))
    assert (a != b)

    a = Card("Riemann", cost=ManaCost({Colour.Blue: 2}))
    assert (a == b)

    a = Card("Riemann", cost=ManaCost({Colour.Blue: 2}), mvid=123)
    assert (a != b)


def test_card_hash():
    def generate_args():
        products = itertools.product(["A"], [ManaCost({Colour.Red: 3}), UNKNOWN], [123, UNKNOWN])
        keyvalue_combos = [{"title": t, "cost": c, "mvid": id} for t, c, id in products]
        return keyvalue_combos

    for kwargs in generate_args():
        a = Card(**kwargs)
        b = Card(**kwargs)

        assert (hash(a) == hash(b))
        assert (a == b)


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

    assert (cost1 != "Riemann")
