from manapool.deck import Deck, Card

import pytest


def test_deck_constructor_bad_inputs():
    with pytest.raises(ValueError):
        Deck(1)

    with pytest.raises(ValueError):
        Deck(Card("Riemann"), Card("Euler"), True)


def test_deck_constructor_empty():
    d = Deck()

    assert d.empty


def test_deck_constructor_not_empty():
    a = Card("Riemann")
    b = Card("Euler")

    d = Deck(a, b)
    assert (len(d) == 2)
    assert (d[0] is a)
    assert (d[1] is b)


def test_deck_empty_equals_empty():
    assert (Deck() == Deck())
