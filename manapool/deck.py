from abc import abstractmethod
from typing import Sequence, Tuple

from card import Card


class Deck(Tuple[Card]):
    """Represents a Deck. Decks are immutable."""

    def __new__(cls, *args: Card):
        """
        Creates a new deck from the given cards.
        :param args: A sequence of cards.

        :raises ValueError:
        """

        def is_not_a_card(c):
            return not isinstance(c, Card)

        if any(is_not_a_card(c) for c in args):
            raise ValueError("An item of cards was not of a Card type.")
        return super(Deck, cls).__new__(cls, tuple(args))

    @property
    def empty(self) -> bool:
        return len(self) == 0


def tally(deck: Deck) -> Sequence[Tuple[Card, int]]:
    """Tallies a Deck: counts each instance of a card. This is a very basic and useful operation.

    :raises ValueError: deck is not a Deck.

    :param deck: The deck to tally.
    :return: A sequence of tuples, where the first member is the card and the second the count.
    """
    if not isinstance(deck, Deck):
        raise ValueError("Expected a Deck.")

    counts = {}
    for card in deck:
        if card in counts:
            counts[card] = counts[card] + 1
        else:
            counts[card] = 1

    return tuple((card, count) for card, count in counts.items())