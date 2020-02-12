from manapool.deck import Deck, Card
from manapool import deck, calc

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
        deck.tally(None)
    with pytest.raises(ValueError):
        deck.tally("Not a Deck")


def test_tally_empty_deck():
    assert (list(deck.tally(Deck())) == [])


def test_tally():
    cards = [Card(n) for n in ["Riemann", "Euler", "Euler", "Riemann", "Gauss"]]
    d = Deck(*cards)

    t = deck.tally(d)

    t = list(t)

    assert (len(t) == 3)

    assert ((Card("Riemann"), 2) in t)
    assert ((Card("Euler"), 2) in t)
    assert ((Card("Gauss"), 1) in t)


# OPENING_HAND TESTS

def test_opening_hand_bad_arguments():
    with pytest.raises(ValueError):
        deck.opening_hand(None)
    with pytest.raises(ValueError):
        deck.opening_hand(Deck(), count="Riemann")
    with pytest.raises(ValueError):
        deck.opening_hand(Deck(), count=2)


def test_opening_hand_zero_count():
    t = deck.opening_hand(Deck(Card("Euler")), count=0)
    assert (t == ())


def test_opening_hand():
    a = Card("A")
    b = Card("B")
    c = Card("C")

    d = Deck(a, b, c)

    t = deck.opening_hand(d, count=1)
    assert (a in t or b in t or c in t)
    assert (len(t) == 1)

    t = deck.opening_hand(d, count=3)
    assert (a in t or b in t or c in t)
    assert (len(t) == 3)

    t = deck.opening_hand(Deck(a, *((b,)*6)))
    assert (len([c for c in t if c == a]) == 1)
    assert (len([c for c in t if c == b]) == 6)


def test_opening_hand_probabilities():
    a = Card("A")
    b = Card("B")
    c = Card("C")

    d = Deck(a, b, *((c,)*7))

    theoretical_a_occurrence = calc.binomial(8, 6)
    theoretical_b_occurrence = calc.binomial(8, 6)
    theoretical_c_occurrence = 2 * calc.binomial(7, 6) + calc.binomial(7, 5) + calc.binomial(7, 7)
    total = calc.binomial(9, 7)

    theoretical_a_occurrence = theoretical_a_occurrence / float(total)
    theoretical_b_occurrence = theoretical_b_occurrence / float(total)
    theoretical_c_occurrence = theoretical_c_occurrence / float(total)

    samples = 10000
    a_hands = 0
    b_hands = 0
    c_hands = 0
    for i in range(0, samples):
        t = deck.opening_hand(d, count=7)
        if a in t:
            a_hands += 1
        if b in t:
            b_hands += 1
        if c in t:
            c_hands += 1

    tolerance = 0.05
    assert (abs((a_hands/float(samples)) - theoretical_a_occurrence) <= tolerance)
    assert (abs((b_hands/float(samples)) - theoretical_b_occurrence) <= tolerance)
    assert (abs((c_hands/float(samples)) - theoretical_c_occurrence) <= tolerance)