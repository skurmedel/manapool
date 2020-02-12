from manapool.deck import Deck, Card, tally

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


def test_deck_contains():
    a = Card("Riemann")
    b = Card("Euler")
    c = Card("Martin-Löf")

    deck = Deck(a, b)

    assert (a in deck)
    assert (b in deck)
    assert (c not in deck)


# TALLY TESTS

def test_tally_bad_arguments():
    with pytest.raises(ValueError):
        tally(None)
    with pytest.raises(ValueError):
        tally("Not a Deck")


def test_tally_empty_deck():
    assert (list(tally(Deck())) == [])


def test_tally():
    cards = [Card(n) for n in ["Riemann", "Euler", "Euler", "Riemann", "Gauss"]]
    deck = Deck(*cards)

    t = tally(deck)

    t = list(t)

    assert (len(t) == 3)

    assert ((Card("Riemann"), 2) in t)
    assert ((Card("Euler"), 2) in t)
    assert ((Card("Gauss"), 1) in t)

