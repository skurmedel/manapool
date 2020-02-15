import pytest
from manapool.card import Card, UNKNOWN, ManaCost, Color
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
    cost = ManaCost({Color.Blue: 2})
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
    b = Card("Riemann", cost=ManaCost({Color.Blue: 2}))
    assert (a != b)

    a = Card("Riemann", cost=ManaCost({Color.Blue: 2}))
    assert (a == b)

    a = Card("Riemann", cost=ManaCost({Color.Blue: 2}), mvid=123)
    assert (a != b)


def test_card_hash():
    def generate_args():
        products = itertools.product(["A"], [ManaCost({Color.Red: 3}), UNKNOWN], [123, UNKNOWN])
        keyvalue_combos = [{"title": t, "cost": c, "mvid": id} for t, c, id in products]
        return keyvalue_combos

    for kwargs in generate_args():
        a = Card(**kwargs)
        b = Card(**kwargs)

        assert (hash(a) == hash(b))
        assert (a == b)


# MANACOST TESTS

def test_manacost_constructor_dict_of_colors():
    cost = ManaCost({Color.Black: 1, Color.Generic: 4})

    assert (cost.black == 1)
    assert (cost.generic == 4)
    for c in (col for col in Color if col not in [Color.Black, Color.Generic]):
        assert (cost[c] == 0)

    cost = ManaCost({c: 1 for c in Color.pure()})
    for c in Color.pure():
        assert (cost[c] == 1)

    with pytest.raises(ValueError):
        cost = ManaCost({Color.Red: 1, Color.Blue: -1})
    with pytest.raises(ValueError):
        cost = ManaCost({Color.Red: 1, Color.Blue: "Euler"})

    cost = ManaCost({Color.Black | Color.Green: 2, Color.Generic: 2})

    assert (cost.black == 2)
    assert (cost.green == 2)
    assert (cost.generic == 2)
    assert (cost.converted == 4)


def test_manacost_constructor_str():
    for s in ["{W}{", "{", "W", "W}", "{U}{WU}", "{W} {U}", "{ R}"]:
        print(s)
        with pytest.raises(ValueError):
            ManaCost(s)

    cases = [
        ("{W}", ManaCost({Color.White: 1})),
        ("{U}", ManaCost({Color.Blue: 1})),
        ("{B}", ManaCost({Color.Black: 1})),
        ("{G}", ManaCost({Color.Green: 1})),
        ("{R}", ManaCost({Color.Red: 1})),
        ("{w}", ManaCost({Color.White: 1})),
        ("{u}", ManaCost({Color.Blue: 1})),
        ("{b}", ManaCost({Color.Black: 1})),
        ("{g}", ManaCost({Color.Green: 1})),
        ("{r}", ManaCost({Color.Red: 1})),
        ("{W}{U}{B}{G}{R}", ManaCost({Color.White: 1, Color.Blue: 1, Color.Black: 1, Color.Green: 1, Color.Red: 1})),
        ("{R}{W}{R}", ManaCost({Color.White: 1, Color.Red: 2})),
        ("{W}{1}{2}", ManaCost({Color.White: 1, Color.Generic: 3})),
        ("{0}", ManaCost({Color.Generic: 0})),
    ]

    for case, expected in cases:
        actual = ManaCost(case)
        assert (actual == expected)


def test_manacost_constructor_none_values():
    with pytest.raises(ValueError):
        cost = ManaCost(None)


def test_manacost_converted():
    cost = ManaCost({Color.Black: 1, Color.Generic: 4})
    assert (cost.converted == 5)

    cost = ManaCost({c: 1 for c in Color.pure()})
    assert (cost.converted == 5)

    cost = ManaCost()
    assert (cost.converted == 0)


def test_manacost_equality():
    cost1 = ManaCost({Color.Black: 1, Color.Generic: 4})
    cost2 = ManaCost({c: 1 for c in Color.pure()})
    cost3 = ManaCost({Color.Black: 1, Color.Generic: 4})

    assert (cost1 != cost2)
    assert (cost1 == cost1)
    assert (cost3 == cost1)

    assert (cost1 != "Riemann")


def test_manacost_repr():
    cases = [
        ("{W}", ManaCost({Color.White: 1})),
        ("{U}", ManaCost({Color.Blue: 1})),
        ("{B}", ManaCost({Color.Black: 1})),
        ("{G}", ManaCost({Color.Green: 1})),
        ("{R}", ManaCost({Color.Red: 1})),
        ("{W}{U}{B}{G}{R}",
         ManaCost({Color.White: 1, Color.Blue: 1, Color.Black: 1, Color.Green: 1, Color.Red: 1})),
        ("{W}{R}{R}", ManaCost({Color.White: 1, Color.Red: 2})),
        ("{W}{3}", ManaCost({Color.White: 1, Color.Generic: 3})),
        ("{0}", ManaCost({Color.Generic: 0})),
    ]

    for expected, case in cases:
        assert (str(case) == expected)